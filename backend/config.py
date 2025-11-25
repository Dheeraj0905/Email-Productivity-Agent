"""Configuration management for Email Productivity Agent."""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # LLM Provider Selection
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")  # "openai" or "ollama"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # General LLM Settings
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "60"))
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "data/email_agent.db")
    
    # Application Configuration
    APP_VERSION: str = "1.0.0"
    APP_NAME: str = "Email Productivity Agent"
    
    # LLM Temperature Settings
    CATEGORIZATION_TEMPERATURE: float = 0.3
    ACTION_EXTRACTION_TEMPERATURE: float = 0.5
    DRAFT_GENERATION_TEMPERATURE: float = 0.8
    AGENT_RESPONSE_TEMPERATURE: float = 0.7
    
    # Conversation Settings
    MAX_CONVERSATION_HISTORY: int = 5
    
    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """
        Validate configuration.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Ensure data directory exists
        db_dir = Path(cls.DATABASE_PATH).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate based on LLM provider
        if cls.LLM_PROVIDER == "openai":
            if not cls.OPENAI_API_KEY:
                return False, "OPENAI_API_KEY not set in environment variables"
            
            if not cls.OPENAI_API_KEY.startswith("sk-"):
                return False, "Invalid OPENAI_API_KEY format"
        
        elif cls.LLM_PROVIDER == "ollama":
            # Ollama doesn't need API key, just check if it's running
            try:
                import requests
                response = requests.get(f"{cls.OLLAMA_BASE_URL}/api/tags", timeout=2)
                if response.status_code != 200:
                    return False, f"Ollama not responding at {cls.OLLAMA_BASE_URL}. Please start Ollama."
            except:
                return False, "Ollama not running. Please start Ollama with: ollama serve"
        
        return True, ""
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get SQLAlchemy database URL."""
        return f"sqlite:///{cls.DATABASE_PATH}"


# Create config instance
config = Config()
