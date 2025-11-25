"""Data models for Email Productivity Agent."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


@dataclass
class Email:
    """Email data model."""
    id: int
    sender: str
    subject: str
    body: str
    timestamp: datetime
    has_attachment: bool = False
    category: Optional[str] = None
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    processed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "sender": self.sender,
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            "has_attachment": self.has_attachment,
            "category": self.category,
            "action_items": self.action_items,
            "processed": self.processed,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Email':
        """Create Email from dictionary."""
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        created_at = data.get("created_at", datetime.utcnow())
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        
        return Email(
            id=data["id"],
            sender=data["sender"],
            subject=data["subject"],
            body=data["body"],
            timestamp=timestamp,
            has_attachment=data.get("has_attachment", False),
            category=data.get("category"),
            action_items=data.get("action_items", []),
            processed=data.get("processed", False),
            created_at=created_at
        )


@dataclass
class Prompt:
    """Prompt template data model."""
    id: Optional[int]
    prompt_type: str
    prompt_text: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "prompt_type": self.prompt_type,
            "prompt_text": self.prompt_text,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }


@dataclass
class Draft:
    """Draft email data model."""
    id: Optional[int]
    email_id: int
    subject: str
    body: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "email_id": self.email_id,
            "subject": self.subject,
            "body": self.body,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }


@dataclass
class ProcessingLog:
    """Processing log data model."""
    id: Optional[int]
    email_id: int
    operation: str
    status: str
    llm_response: Optional[str] = None
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "email_id": self.email_id,
            "operation": self.operation,
            "status": self.status,
            "llm_response": self.llm_response,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp
        }


@dataclass
class AgentMessage:
    """Agent conversation message."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            "metadata": self.metadata
        }
