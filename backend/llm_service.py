"""OpenAI LLM service integration."""
import logging
import time
import json
from typing import Optional, List, Dict, Any, Generator
from openai import OpenAI, APIError, APITimeoutError, RateLimitError

from backend.config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """OpenAI LLM service manager with retry logic and error handling."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
        self.max_retries = config.MAX_RETRIES
        self.timeout = config.TIMEOUT_SECONDS
        self.total_tokens_used = 0
    
    def _call_llm(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ) -> Optional[str]:
        """
        Call OpenAI API with retry logic.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            stream: Whether to stream response
            
        Returns:
            LLM response text or None on failure
        """
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=self.timeout,
                    stream=stream
                )
                
                if stream:
                    return response  # Return generator for streaming
                
                # Track token usage
                if hasattr(response, 'usage') and response.usage:
                    self.total_tokens_used += response.usage.total_tokens
                    logger.info(f"Tokens used: {response.usage.total_tokens} (Total: {self.total_tokens_used})")
                
                return response.choices[0].message.content
                
            except RateLimitError as e:
                logger.warning(f"Rate limit hit (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error("Max retries reached for rate limit")
                    return None
                    
            except APITimeoutError as e:
                logger.warning(f"API timeout (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error("Max retries reached for timeout")
                    return None
                    
            except APIError as e:
                logger.error(f"API error (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                else:
                    logger.error("Max retries reached for API error")
                    return None
                    
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return None
        
        return None
    
    def categorize_email(self, email_content: str, categorization_prompt: str) -> Optional[str]:
        """
        Categorize email using LLM.
        
        Args:
            email_content: Email body to categorize
            categorization_prompt: Prompt template for categorization
            
        Returns:
            Category name or None on failure
        """
        prompt = categorization_prompt.format(email_content=email_content)
        messages = [
            {"role": "system", "content": "You are an email classification expert. Respond with ONLY the category name."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(
            messages=messages,
            temperature=config.CATEGORIZATION_TEMPERATURE,
            max_tokens=50
        )
        
        if response:
            # Extract category from response (handle extra text)
            category = response.strip()
            valid_categories = ["Important", "Newsletter", "Spam", "To-Do"]
            for cat in valid_categories:
                if cat.lower() in category.lower():
                    return cat
            return category
        
        return None
    
    def extract_action_items(
        self,
        email_content: str,
        action_prompt: str
    ) -> List[Dict[str, Any]]:
        """
        Extract action items from email.
        
        Args:
            email_content: Email body to analyze
            action_prompt: Prompt template for action extraction
            
        Returns:
            List of action item dictionaries
        """
        prompt = action_prompt.format(email_content=email_content)
        messages = [
            {"role": "system", "content": "You are an expert at extracting actionable tasks from emails. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(
            messages=messages,
            temperature=config.ACTION_EXTRACTION_TEMPERATURE,
            max_tokens=500
        )
        
        if response:
            try:
                # Try to parse JSON response
                # Handle cases where response might have extra text
                response = response.strip()
                
                # Find JSON array in response
                start_idx = response.find('[')
                end_idx = response.rfind(']')
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx + 1]
                    action_items = json.loads(json_str)
                    return action_items if isinstance(action_items, list) else []
                else:
                    logger.warning("No JSON array found in action extraction response")
                    return []
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse action items JSON: {e}")
                logger.error(f"Response was: {response}")
                return []
        
        return []
    
    def generate_reply(
        self,
        email_content: str,
        context: str,
        reply_prompt: str,
        user_instruction: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate draft reply to email.
        
        Args:
            email_content: Original email to reply to
            context: Additional context about the email
            reply_prompt: Prompt template for reply generation
            user_instruction: Optional specific instructions from user
            
        Returns:
            Draft reply text or None on failure
        """
        prompt = reply_prompt.format(email_content=email_content)
        
        if user_instruction:
            prompt += f"\n\nAdditional Instructions: {user_instruction}"
        
        messages = [
            {"role": "system", "content": "You are a professional email assistant. Write clear, concise, and appropriate email responses."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(
            messages=messages,
            temperature=config.DRAFT_GENERATION_TEMPERATURE,
            max_tokens=800
        )
        
        return response
    
    def answer_query(
        self,
        query: str,
        email_context: Optional[str] = None,
        prompt_context: Optional[str] = None,
        conversation_history: List[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        Answer user query about emails using agent logic.
        
        Args:
            query: User's question or request
            email_context: Relevant email content for context
            prompt_context: Additional prompt configuration context
            conversation_history: Previous messages in conversation
            
        Returns:
            Agent response or None on failure
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an intelligent email productivity assistant. "
                    "Help users manage their inbox, understand emails, and draft responses. "
                    "Be concise, helpful, and professional. "
                    "If you reference specific emails, cite them clearly."
                )
            }
        ]
        
        # Add conversation history (last N messages)
        if conversation_history:
            history_limit = config.MAX_CONVERSATION_HISTORY
            messages.extend(conversation_history[-history_limit:])
        
        # Build context-aware query
        full_query = query
        if email_context:
            full_query = f"Email Context:\n{email_context}\n\nUser Query: {query}"
        
        if prompt_context:
            full_query += f"\n\nPrompt Configuration: {prompt_context}"
        
        messages.append({"role": "user", "content": full_query})
        
        response = self._call_llm(
            messages=messages,
            temperature=config.AGENT_RESPONSE_TEMPERATURE,
            max_tokens=1000
        )
        
        return response
    
    def stream_response(
        self,
        query: str,
        email_context: Optional[str] = None,
        conversation_history: List[Dict[str, str]] = None
    ) -> Generator[str, None, None]:
        """
        Stream agent response for chat interface.
        
        Args:
            query: User's question
            email_context: Relevant email content
            conversation_history: Previous messages
            
        Yields:
            Response chunks as they arrive
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an intelligent email productivity assistant. "
                    "Help users manage their inbox efficiently."
                )
            }
        ]
        
        if conversation_history:
            history_limit = config.MAX_CONVERSATION_HISTORY
            messages.extend(conversation_history[-history_limit:])
        
        full_query = query
        if email_context:
            full_query = f"Email Context:\n{email_context}\n\nUser Query: {query}"
        
        messages.append({"role": "user", "content": full_query})
        
        try:
            stream = self._call_llm(
                messages=messages,
                temperature=config.AGENT_RESPONSE_TEMPERATURE,
                max_tokens=1000,
                stream=True
            )
            
            if stream:
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                        
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"Error: {str(e)}"
    
    def get_token_usage(self) -> int:
        """Get total tokens used in this session."""
        return self.total_tokens_used


# Singleton LLM service instance
llm_service = LLMService()
