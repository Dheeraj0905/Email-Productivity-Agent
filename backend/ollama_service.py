"""Ollama LLM service integration (Free, Local AI)."""
import logging
import time
import json
import requests
from typing import Optional, List, Dict, Any, Generator

from backend.config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaService:
    """Ollama LLM service manager - completely free local AI."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama API endpoint
            model: Model name to use (llama3.2, mistral, etc.)
        """
        self.base_url = base_url
        self.model = model
        self.max_retries = 3
        self.timeout = 60
        self.total_tokens_used = 0
    
    def _call_llm(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ) -> Optional[str]:
        """
        Call Ollama API with retry logic.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            stream: Whether to stream response
            
        Returns:
            LLM response text or None on failure
        """
        # Convert messages to Ollama format (simple prompt)
        prompt = self._messages_to_prompt(messages)
        
        for attempt in range(self.max_retries):
            try:
                url = f"{self.base_url}/api/generate"
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens
                    }
                }
                
                response = requests.post(
                    url,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result.get("response", "")
                    
                    # Estimate tokens (rough approximation)
                    self.total_tokens_used += len(content.split()) * 1.3
                    
                    return content
                elif response.status_code == 404:
                    logger.error(f"Model '{self.model}' not found. Please run: ollama pull {self.model}")
                    return None
                else:
                    logger.warning(f"Ollama API returned status {response.status_code}")
                    
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Cannot connect to Ollama. Is it running? Error: {e}")
                if attempt < self.max_retries - 1:
                    logger.info("Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    logger.error("Please start Ollama: Run 'ollama serve' in terminal")
                    return None
                    
            except requests.exceptions.Timeout as e:
                logger.warning(f"Timeout (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                else:
                    return None
                    
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return None
        
        return None
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to a single prompt."""
        prompt_parts = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}\n")
            elif role == "user":
                prompt_parts.append(f"User: {content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}\n")
        
        prompt_parts.append("Assistant: ")
        return "\n".join(prompt_parts)
    
    def categorize_email(self, email_content: str, categorization_prompt: str) -> Optional[str]:
        """
        Categorize email using LLM.
        
        Args:
            email_content: Email body to categorize
            categorization_prompt: Prompt template for categorization
            
        Returns:
            Category name or None on failure
        """
        # Replace placeholder safely
        prompt = categorization_prompt.replace("{email_content}", email_content)
        messages = [
            {"role": "system", "content": "You are an email classification expert. Respond with ONLY the category name."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(
            messages=messages,
            temperature=0.3,
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
        # Replace placeholder safely to avoid issues with JSON braces in prompt
        prompt = action_prompt.replace("{email_content}", email_content)
        messages = [
            {"role": "system", "content": "You are an expert at extracting actionable tasks from emails. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(
            messages=messages,
            temperature=0.5,
            max_tokens=500
        )
        
        if response:
            try:
                # Try to parse JSON response
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
        # Replace placeholder safely
        prompt = reply_prompt.replace("{email_content}", email_content)
        
        if user_instruction:
            prompt += f"\n\nAdditional Instructions: {user_instruction}"
        
        messages = [
            {"role": "system", "content": "You are a professional email assistant. Write clear, concise, and appropriate email responses."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._call_llm(
            messages=messages,
            temperature=0.8,
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
        
        # Add conversation history (last 5 messages)
        if conversation_history:
            messages.extend(conversation_history[-5:])
        
        # Build context-aware query
        full_query = query
        if email_context:
            full_query = f"Email Context:\n{email_context}\n\nUser Query: {query}"
        
        if prompt_context:
            full_query += f"\n\nPrompt Configuration: {prompt_context}"
        
        messages.append({"role": "user", "content": full_query})
        
        response = self._call_llm(
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response
    
    def get_token_usage(self) -> int:
        """Get estimated tokens used in this session."""
        return int(self.total_tokens_used)
    
    def check_health(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                
                # Check if our model is available
                if any(self.model in name for name in model_names):
                    logger.info(f"✓ Ollama is running with model: {self.model}")
                    return True
                else:
                    logger.warning(f"Model '{self.model}' not found. Available: {model_names}")
                    logger.info(f"Run: ollama pull {self.model}")
                    return False
            return False
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False


# Singleton Ollama service instance
ollama_service = OllamaService()
