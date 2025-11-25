"""Unified LLM service that works with both OpenAI and Ollama."""
import logging
from typing import Optional, List, Dict, Any

from backend.config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedLLMService:
    """Unified LLM service that automatically uses OpenAI or Ollama based on config."""
    
    def __init__(self):
        """Initialize the appropriate LLM service based on configuration."""
        self.provider = config.LLM_PROVIDER
        self.service = None
        
        logger.info(f"Initializing LLM service with provider: {self.provider}")
        
        if self.provider == "ollama":
            from backend.ollama_service import OllamaService
            self.service = OllamaService(
                base_url=config.OLLAMA_BASE_URL,
                model=config.OLLAMA_MODEL
            )
            logger.info(f"✓ Using Ollama (FREE) with model: {config.OLLAMA_MODEL}")
            
            # Check health
            if self.service.check_health():
                logger.info("✓ Ollama is ready!")
            else:
                logger.warning("⚠️ Ollama model not found. Run: ollama pull llama3.2")
                
        elif self.provider == "openai":
            from backend.llm_service import LLMService
            self.service = LLMService()
            logger.info(f"✓ Using OpenAI with model: {config.OPENAI_MODEL}")
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")
    
    def categorize_email(self, email_content: str, categorization_prompt: str) -> Optional[str]:
        """Categorize email using configured LLM."""
        return self.service.categorize_email(email_content, categorization_prompt)
    
    def extract_action_items(self, email_content: str, action_prompt: str) -> List[Dict[str, Any]]:
        """Extract action items using configured LLM."""
        return self.service.extract_action_items(email_content, action_prompt)
    
    def generate_reply(
        self,
        email_content: str,
        context: str,
        reply_prompt: str,
        user_instruction: Optional[str] = None
    ) -> Optional[str]:
        """Generate reply using configured LLM."""
        return self.service.generate_reply(email_content, context, reply_prompt, user_instruction)
    
    def answer_query(
        self,
        query: str,
        email_context: Optional[str] = None,
        prompt_context: Optional[str] = None,
        conversation_history: List[Dict[str, str]] = None
    ) -> Optional[str]:
        """Answer query using configured LLM."""
        return self.service.answer_query(query, email_context, prompt_context, conversation_history)
    
    def get_token_usage(self) -> int:
        """Get token/request usage."""
        return self.service.get_token_usage()


# Singleton unified service instance
unified_llm_service = UnifiedLLMService()
