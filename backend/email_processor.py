"""Email processing pipeline."""
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

from backend.database import db
from backend.unified_llm_service import unified_llm_service
from backend.models import Email, ProcessingLog

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailProcessor:
    """Email processing pipeline manager."""
    
    def __init__(self):
        """Initialize processor."""
        self.db = db
        self.llm = unified_llm_service
    
    def load_mock_inbox(self, json_path: str = "data/mock_inbox.json") -> int:
        """
        Load mock emails from JSON file into database.
        
        Args:
            json_path: Path to JSON file containing mock emails
            
        Returns:
            Number of emails loaded
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                emails_data = json.load(f)
            
            loaded_count = 0
            for email_data in emails_data:
                email = Email.from_dict(email_data)
                try:
                    self.db.insert_email(email)
                    loaded_count += 1
                except Exception as e:
                    logger.warning(f"Skipping duplicate email ID {email.id}: {e}")
            
            logger.info(f"Loaded {loaded_count} emails from {json_path}")
            return loaded_count
            
        except FileNotFoundError:
            logger.error(f"Mock inbox file not found: {json_path}")
            return 0
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in mock inbox: {e}")
            return 0
        except Exception as e:
            logger.error(f"Error loading mock inbox: {e}")
            return 0
    
    def process_email(self, email_id: int) -> bool:
        """
        Process single email through categorization and action extraction pipeline.
        
        Args:
            email_id: ID of email to process
            
        Returns:
            True if processing succeeded, False otherwise
        """
        # Fetch email from database
        email = self.db.get_email(email_id)
        if not email:
            logger.error(f"Email {email_id} not found")
            return False
        
        logger.info(f"Processing email {email_id}: {email.subject}")
        
        # Step 1: Categorize email
        category = self._categorize_email(email)
        if not category:
            self._log_processing(email_id, "categorization", "failed", error="LLM categorization failed")
            return False
        
        # Step 2: Extract action items
        action_items = self._extract_action_items(email)
        
        # Step 3: Update email in database
        try:
            self.db.update_email(
                email_id=email_id,
                category=category,
                action_items=action_items,
                processed=True
            )
            
            self._log_processing(
                email_id,
                "complete_processing",
                "success",
                llm_response=f"Category: {category}, Actions: {len(action_items)}"
            )
            
            logger.info(f"Successfully processed email {email_id}: {category}, {len(action_items)} actions")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update email {email_id}: {e}")
            self._log_processing(email_id, "database_update", "failed", error=str(e))
            return False
    
    def batch_process_emails(self, email_ids: List[int]) -> Dict[str, Any]:
        """
        Process multiple emails in batch.
        
        Args:
            email_ids: List of email IDs to process
            
        Returns:
            Dictionary with processing statistics
        """
        results = {
            "total": len(email_ids),
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        for email_id in email_ids:
            try:
                if self.process_email(email_id):
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(f"Email {email_id} processing failed")
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Email {email_id}: {str(e)}")
                logger.error(f"Error processing email {email_id}: {e}")
        
        logger.info(f"Batch processing complete: {results['successful']}/{results['total']} successful")
        return results
    
    def _categorize_email(self, email: Email) -> Optional[str]:
        """
        Categorize email using LLM.
        
        Args:
            email: Email object to categorize
            
        Returns:
            Category name or None on failure
        """
        # Get categorization prompt from database
        prompt_obj = self.db.get_prompt("categorization")
        if not prompt_obj:
            logger.error("Categorization prompt not found in database")
            return None
        
        # Build email content string
        email_content = f"From: {email.sender}\nSubject: {email.subject}\n\n{email.body}"
        
        # Call LLM
        category = self.llm.categorize_email(email_content, prompt_obj.prompt_text)
        
        if category:
            self._log_processing(
                email.id,
                "categorization",
                "success",
                llm_response=category
            )
        else:
            self._log_processing(
                email.id,
                "categorization",
                "failed",
                error="LLM returned no category"
            )
        
        return category
    
    def _extract_action_items(self, email: Email) -> List[Dict[str, Any]]:
        """
        Extract action items from email using LLM.
        
        Args:
            email: Email object to analyze
            
        Returns:
            List of action item dictionaries
        """
        # Get action extraction prompt from database
        prompt_obj = self.db.get_prompt("action_extraction")
        if not prompt_obj:
            logger.warning("Action extraction prompt not found in database")
            return []
        
        # Build email content string
        email_content = f"From: {email.sender}\nSubject: {email.subject}\n\n{email.body}"
        
        # Call LLM
        action_items = self.llm.extract_action_items(email_content, prompt_obj.prompt_text)
        
        if action_items:
            self._log_processing(
                email.id,
                "action_extraction",
                "success",
                llm_response=f"Found {len(action_items)} action items"
            )
        else:
            self._log_processing(
                email.id,
                "action_extraction",
                "success",
                llm_response="No action items found"
            )
        
        return action_items
    
    def _log_processing(
        self,
        email_id: int,
        operation: str,
        status: str,
        llm_response: str = None,
        error: str = None
    ):
        """
        Log processing operation to database.
        
        Args:
            email_id: Email being processed
            operation: Type of operation
            status: Status (success/failed)
            llm_response: LLM response text
            error: Error message if failed
        """
        log = ProcessingLog(
            id=None,
            email_id=email_id,
            operation=operation,
            status=status,
            llm_response=llm_response,
            error_message=error,
            timestamp=datetime.utcnow()
        )
        
        try:
            self.db.insert_log(log)
        except Exception as e:
            logger.error(f"Failed to insert processing log: {e}")


# Singleton processor instance
email_processor = EmailProcessor()
