"""Database operations for Email Productivity Agent."""
import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from backend.config import config
from backend.models import Email, Prompt, Draft, ProcessingLog

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager."""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection."""
        self.db_path = db_path or config.DATABASE_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Emails table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY,
                    sender TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    body TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    has_attachment INTEGER DEFAULT 0,
                    category TEXT,
                    action_items_json TEXT,
                    processed INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Prompts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_type TEXT NOT NULL UNIQUE,
                    prompt_text TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            # Drafts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS drafts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email_id INTEGER NOT NULL,
                    subject TEXT NOT NULL,
                    body TEXT NOT NULL,
                    metadata_json TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (email_id) REFERENCES emails(id)
                )
            """)
            
            # Processing logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email_id INTEGER NOT NULL,
                    operation TEXT NOT NULL,
                    status TEXT NOT NULL,
                    llm_response TEXT,
                    error_message TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (email_id) REFERENCES emails(id)
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_emails_category ON emails(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_emails_processed ON emails(processed)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_emails_timestamp ON emails(timestamp)")
            
            logger.info("Database initialized successfully")
    
    # Email operations
    def insert_email(self, email: Email) -> int:
        """Insert email into database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO emails (id, sender, subject, body, timestamp, has_attachment, 
                                    category, action_items_json, processed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                email.id,
                email.sender,
                email.subject,
                email.body,
                email.timestamp.isoformat() if isinstance(email.timestamp, datetime) else email.timestamp,
                int(email.has_attachment),
                email.category,
                json.dumps(email.action_items),
                int(email.processed),
                email.created_at.isoformat()
            ))
            return cursor.lastrowid
    
    def get_email(self, email_id: int) -> Optional[Email]:
        """Get email by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM emails WHERE id = ?", (email_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_email(row)
            return None
    
    def get_all_emails(self, limit: int = 100) -> List[Email]:
        """Get all emails."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM emails ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [self._row_to_email(row) for row in rows]
    
    def update_email(self, email_id: int, category: str = None, 
                     action_items: List[Dict] = None, processed: bool = None):
        """Update email fields."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            updates = []
            params = []
            
            if category is not None:
                updates.append("category = ?")
                params.append(category)
            
            if action_items is not None:
                updates.append("action_items_json = ?")
                params.append(json.dumps(action_items))
            
            if processed is not None:
                updates.append("processed = ?")
                params.append(int(processed))
            
            if updates:
                query = f"UPDATE emails SET {', '.join(updates)} WHERE id = ?"
                params.append(email_id)
                cursor.execute(query, params)
    
    def search_emails(self, query: str = None, category: str = None, 
                      processed: bool = None) -> List[Email]:
        """Search emails with filters."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            conditions = []
            params = []
            
            if query:
                conditions.append("(subject LIKE ? OR body LIKE ? OR sender LIKE ?)")
                search_term = f"%{query}%"
                params.extend([search_term, search_term, search_term])
            
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            if processed is not None:
                conditions.append("processed = ?")
                params.append(int(processed))
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            cursor.execute(f"SELECT * FROM emails WHERE {where_clause} ORDER BY timestamp DESC", params)
            rows = cursor.fetchall()
            return [self._row_to_email(row) for row in rows]
    
    # Prompt operations
    def insert_prompt(self, prompt: Prompt) -> int:
        """Insert or update prompt."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO prompts (prompt_type, prompt_text, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                prompt.prompt_type,
                prompt.prompt_text,
                int(prompt.is_active),
                prompt.created_at.isoformat(),
                datetime.utcnow().isoformat()
            ))
            return cursor.lastrowid
    
    def get_prompt(self, prompt_type: str) -> Optional[Prompt]:
        """Get active prompt by type."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM prompts WHERE prompt_type = ? AND is_active = 1
            """, (prompt_type,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_prompt(row)
            return None
    
    def get_all_prompts(self) -> List[Prompt]:
        """Get all active prompts."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prompts WHERE is_active = 1")
            rows = cursor.fetchall()
            return [self._row_to_prompt(row) for row in rows]
    
    # Draft operations
    def insert_draft(self, draft: Draft) -> int:
        """Insert draft."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO drafts (email_id, subject, body, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                draft.email_id,
                draft.subject,
                draft.body,
                json.dumps(draft.metadata),
                draft.created_at.isoformat()
            ))
            return cursor.lastrowid
    
    def get_drafts(self, email_id: int = None) -> List[Draft]:
        """Get drafts, optionally filtered by email_id."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if email_id:
                cursor.execute("SELECT * FROM drafts WHERE email_id = ? ORDER BY created_at DESC", (email_id,))
            else:
                cursor.execute("SELECT * FROM drafts ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [self._row_to_draft(row) for row in rows]
    
    def delete_draft(self, draft_id: int):
        """Delete draft."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM drafts WHERE id = ?", (draft_id,))
    
    # Processing log operations
    def insert_log(self, log: ProcessingLog) -> int:
        """Insert processing log."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO processing_logs (email_id, operation, status, llm_response, error_message, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                log.email_id,
                log.operation,
                log.status,
                log.llm_response,
                log.error_message,
                log.timestamp.isoformat()
            ))
            return cursor.lastrowid
    
    def get_logs(self, email_id: int = None, limit: int = 50) -> List[ProcessingLog]:
        """Get processing logs."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if email_id:
                cursor.execute("""
                    SELECT * FROM processing_logs WHERE email_id = ? 
                    ORDER BY timestamp DESC LIMIT ?
                """, (email_id, limit))
            else:
                cursor.execute("SELECT * FROM processing_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [self._row_to_log(row) for row in rows]
    
    # Helper methods
    def _row_to_email(self, row: sqlite3.Row) -> Email:
        """Convert database row to Email object."""
        action_items = json.loads(row['action_items_json']) if row['action_items_json'] else []
        timestamp = datetime.fromisoformat(row['timestamp']) if row['timestamp'] else datetime.utcnow()
        created_at = datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.utcnow()
        
        return Email(
            id=row['id'],
            sender=row['sender'],
            subject=row['subject'],
            body=row['body'],
            timestamp=timestamp,
            has_attachment=bool(row['has_attachment']),
            category=row['category'],
            action_items=action_items,
            processed=bool(row['processed']),
            created_at=created_at
        )
    
    def _row_to_prompt(self, row: sqlite3.Row) -> Prompt:
        """Convert database row to Prompt object."""
        return Prompt(
            id=row['id'],
            prompt_type=row['prompt_type'],
            prompt_text=row['prompt_text'],
            is_active=bool(row['is_active']),
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )
    
    def _row_to_draft(self, row: sqlite3.Row) -> Draft:
        """Convert database row to Draft object."""
        metadata = json.loads(row['metadata_json']) if row['metadata_json'] else {}
        return Draft(
            id=row['id'],
            email_id=row['email_id'],
            subject=row['subject'],
            body=row['body'],
            metadata=metadata,
            created_at=datetime.fromisoformat(row['created_at'])
        )
    
    def _row_to_log(self, row: sqlite3.Row) -> ProcessingLog:
        """Convert database row to ProcessingLog object."""
        return ProcessingLog(
            id=row['id'],
            email_id=row['email_id'],
            operation=row['operation'],
            status=row['status'],
            llm_response=row['llm_response'],
            error_message=row['error_message'],
            timestamp=datetime.fromisoformat(row['timestamp'])
        )


# Singleton database instance
db = Database()


def init_database():
    """Initialize database (for use in setup scripts)."""
    db.init_database()
    logger.info("Database initialized successfully")


if __name__ == "__main__":
    init_database()
