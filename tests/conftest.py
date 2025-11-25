"""Test configuration and fixtures."""
import pytest
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import Database
from backend.config import config


@pytest.fixture
def test_db():
    """Create a test database."""
    db_path = "test_email_agent.db"
    test_database = Database(db_path)
    test_database.init_database()
    
    yield test_database
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return {
        "id": 1,
        "sender": "test@example.com",
        "subject": "Test Email",
        "body": "This is a test email body with action items: Please review the document by Friday.",
        "timestamp": "2025-11-24T10:00:00Z",
        "has_attachment": False
    }


@pytest.fixture
def sample_prompt_data():
    """Sample prompt data for testing."""
    return {
        "prompt_type": "test_categorization",
        "prompt_text": "Categorize this email: {email_content}",
        "temperature": 0.3
    }
