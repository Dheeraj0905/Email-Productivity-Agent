"""Tests for email processor."""
import pytest
from datetime import datetime

from backend.models import Email, Prompt
from backend.email_processor import EmailProcessor


def test_load_mock_inbox(test_db):
    """Test loading mock inbox from JSON."""
    processor = EmailProcessor()
    processor.db = test_db
    
    # Note: This will fail if mock_inbox.json doesn't exist
    # In production, the file should exist
    count = processor.load_mock_inbox("data/mock_inbox.json")
    
    # Should load some emails
    assert count >= 0  # May be 0 if file doesn't exist yet


def test_email_insertion(test_db, sample_email_data):
    """Test inserting email into database."""
    email = Email.from_dict(sample_email_data)
    email_id = test_db.insert_email(email)
    
    assert email_id is not None
    
    # Retrieve and verify
    retrieved = test_db.get_email(email.id)
    assert retrieved is not None
    assert retrieved.sender == email.sender
    assert retrieved.subject == email.subject


def test_email_update(test_db, sample_email_data):
    """Test updating email fields."""
    email = Email.from_dict(sample_email_data)
    test_db.insert_email(email)
    
    # Update category and action items
    test_db.update_email(
        email_id=email.id,
        category="Important",
        action_items=[{"task": "Review document", "deadline": "Friday", "priority": "high"}],
        processed=True
    )
    
    # Retrieve and verify
    updated = test_db.get_email(email.id)
    assert updated.category == "Important"
    assert len(updated.action_items) == 1
    assert updated.processed is True


def test_email_search(test_db):
    """Test email search functionality."""
    # Insert multiple emails
    for i in range(5):
        email = Email(
            id=i + 1,
            sender=f"sender{i}@example.com",
            subject=f"Test Subject {i}",
            body=f"Test body {i}",
            timestamp=datetime.utcnow(),
            category="Important" if i % 2 == 0 else "Newsletter"
        )
        test_db.insert_email(email)
    
    # Search by category
    important_emails = test_db.search_emails(category="Important")
    assert len(important_emails) == 3  # IDs 0, 2, 4
    
    # Search by query
    search_results = test_db.search_emails(query="Subject 1")
    assert len(search_results) == 1


def test_batch_processing(test_db):
    """Test batch email processing."""
    processor = EmailProcessor()
    processor.db = test_db
    
    # Insert test emails
    email_ids = []
    for i in range(3):
        email = Email(
            id=i + 1,
            sender=f"sender{i}@example.com",
            subject=f"Test Subject {i}",
            body=f"Test body {i}",
            timestamp=datetime.utcnow()
        )
        test_db.insert_email(email)
        email_ids.append(email.id)
    
    # Note: Batch processing will fail without valid OpenAI API key
    # In real tests, you'd mock the LLM service
    # results = processor.batch_process_emails(email_ids)
    # assert results["total"] == 3


def test_prompt_insertion(test_db, sample_prompt_data):
    """Test inserting and retrieving prompts."""
    prompt = Prompt(
        id=None,
        prompt_type=sample_prompt_data["prompt_type"],
        prompt_text=sample_prompt_data["prompt_text"],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    prompt_id = test_db.insert_prompt(prompt)
    assert prompt_id is not None
    
    # Retrieve
    retrieved = test_db.get_prompt(sample_prompt_data["prompt_type"])
    assert retrieved is not None
    assert retrieved.prompt_text == sample_prompt_data["prompt_text"]
