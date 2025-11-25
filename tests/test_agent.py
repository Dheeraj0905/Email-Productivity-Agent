"""Tests for agent logic."""
import pytest
from datetime import datetime

from backend.models import Email, AgentMessage
from backend.agent_logic import EmailAgent


def test_agent_initialization():
    """Test agent initialization."""
    agent = EmailAgent()
    assert agent is not None
    assert agent.conversation_history == []


def test_is_inbox_query():
    """Test inbox query detection."""
    agent = EmailAgent()
    
    # Should be inbox queries
    assert agent._is_inbox_query("show me all emails") is True
    assert agent._is_inbox_query("what urgent emails do I have?") is True
    assert agent._is_inbox_query("list all tasks") is True
    
    # Should not be inbox queries
    assert agent._is_inbox_query("summarize this") is False
    assert agent._is_inbox_query("thanks for the info") is False


def test_build_email_context(test_db, sample_email_data):
    """Test building email context."""
    agent = EmailAgent()
    agent.db = test_db
    
    email = Email.from_dict(sample_email_data)
    test_db.insert_email(email)
    
    context = agent._build_email_context(email)
    
    assert "Email ID:" in context
    assert email.sender in context
    assert email.subject in context


def test_extract_tasks_from_email(test_db):
    """Test extracting tasks from processed email."""
    agent = EmailAgent()
    agent.db = test_db
    
    # Create email with action items
    email = Email(
        id=1,
        sender="test@example.com",
        subject="Project Tasks",
        body="Please complete these tasks",
        timestamp=datetime.utcnow(),
        action_items=[
            {"task": "Review document", "deadline": "Friday", "priority": "high"},
            {"task": "Send report", "deadline": None, "priority": "medium"}
        ],
        processed=True
    )
    test_db.insert_email(email)
    
    result = agent.extract_tasks_from_email(email.id)
    
    assert "Action Items" in result
    assert "Review document" in result
    assert "Send report" in result


def test_search_inbox(test_db):
    """Test inbox search functionality."""
    agent = EmailAgent()
    agent.db = test_db
    
    # Insert test emails
    for i in range(3):
        email = Email(
            id=i + 1,
            sender=f"sender{i}@example.com",
            subject=f"Important Meeting {i}",
            body=f"Meeting details {i}",
            timestamp=datetime.utcnow(),
            category="Important"
        )
        test_db.insert_email(email)
    
    result = agent.search_inbox("Meeting")
    
    assert "Found" in result
    assert "3 email(s)" in result


def test_get_urgent_emails(test_db):
    """Test getting urgent emails."""
    agent = EmailAgent()
    agent.db = test_db
    
    # Insert important and to-do emails
    email1 = Email(
        id=1,
        sender="urgent@example.com",
        subject="Urgent Task",
        body="Please do this immediately",
        timestamp=datetime.utcnow(),
        category="Important",
        processed=True
    )
    email2 = Email(
        id=2,
        sender="todo@example.com",
        subject="To-Do Item",
        body="Task to complete",
        timestamp=datetime.utcnow(),
        category="To-Do",
        processed=True
    )
    
    test_db.insert_email(email1)
    test_db.insert_email(email2)
    
    result = agent.get_urgent_emails()
    
    assert "Urgent" in result or "Important" in result
    assert "2" in result


def test_conversation_message():
    """Test agent message creation."""
    msg = AgentMessage(
        role="user",
        content="Test message",
        timestamp=datetime.utcnow()
    )
    
    assert msg.role == "user"
    assert msg.content == "Test message"
    assert msg.metadata == {}
    
    # Test to_dict
    msg_dict = msg.to_dict()
    assert msg_dict["role"] == "user"
    assert msg_dict["content"] == "Test message"


# Note: Testing actual LLM calls requires mocking or valid API keys
# In production, use pytest-mock or unittest.mock to mock LLM responses
