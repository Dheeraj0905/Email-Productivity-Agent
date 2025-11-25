"""Agent logic for handling user queries and managing conversations."""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from backend.database import db
from backend.unified_llm_service import unified_llm_service
from backend.models import Email, Draft, AgentMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailAgent:
    """Intelligent email agent for handling user queries."""
    
    def __init__(self):
        """Initialize agent."""
        self.db = db
        self.llm = unified_llm_service
        self.conversation_history: List[Dict[str, str]] = []
    
    def handle_query(
        self,
        user_query: str,
        selected_email_id: Optional[int] = None,
        conversation_history: List[AgentMessage] = None
    ) -> str:
        """
        Handle user query with context awareness.
        
        Args:
            user_query: User's question or request
            selected_email_id: Currently selected email ID for context
            conversation_history: Previous conversation messages
            
        Returns:
            Agent response text
        """
        logger.info(f"Handling query: {user_query[:50]}...")
        
        # Build conversation history for LLM
        messages = []
        if conversation_history:
            messages = [
                {"role": msg.role, "content": msg.content}
                for msg in conversation_history[-5:]  # Last 5 messages
            ]
        
        # Determine query type and gather context
        email_context = None
        
        if selected_email_id:
            # Single email query - fetch email details
            email = self.db.get_email(selected_email_id)
            if email:
                email_context = self._build_email_context(email)
        
        # Check for inbox-wide queries
        elif self._is_inbox_query(user_query):
            email_context = self._build_inbox_context(user_query)
        
        # Call LLM with context
        response = self.llm.answer_query(
            query=user_query,
            email_context=email_context,
            conversation_history=messages
        )
        
        if response:
            return response
        else:
            return "I apologize, but I'm having trouble processing your request. Please try again."
    
    def generate_draft(
        self,
        email_id: int,
        user_instruction: Optional[str] = None
    ) -> Optional[Draft]:
        """
        Generate draft reply for an email.
        
        Args:
            email_id: Email to reply to
            user_instruction: Optional specific instructions
            
        Returns:
            Draft object or None on failure
        """
        # Fetch email
        email = self.db.get_email(email_id)
        if not email:
            logger.error(f"Email {email_id} not found")
            return None
        
        # Get reply prompt
        prompt_obj = self.db.get_prompt("auto_reply")
        if not prompt_obj:
            logger.error("Auto-reply prompt not found")
            return None
        
        # Build email content
        email_content = f"From: {email.sender}\nSubject: {email.subject}\n\n{email.body}"
        
        # Generate reply
        reply_body = self.llm.generate_reply(
            email_content=email_content,
            context=f"Category: {email.category}",
            reply_prompt=prompt_obj.prompt_text,
            user_instruction=user_instruction
        )
        
        if not reply_body:
            logger.error("Failed to generate reply")
            return None
        
        # Create draft object
        draft = Draft(
            id=None,
            email_id=email_id,
            subject=f"Re: {email.subject}",
            body=reply_body,
            metadata={
                "original_sender": email.sender,
                "original_subject": email.subject,
                "user_instruction": user_instruction,
                "prompt_used": "auto_reply",
                "generated_at": datetime.utcnow().isoformat()
            },
            created_at=datetime.utcnow()
        )
        
        # Save draft to database
        try:
            draft.id = self.db.insert_draft(draft)
            logger.info(f"Created draft {draft.id} for email {email_id}")
            return draft
        except Exception as e:
            logger.error(f"Failed to save draft: {e}")
            return None
    
    def summarize_email(self, email_id: int) -> str:
        """
        Generate summary of an email.
        
        Args:
            email_id: Email to summarize
            
        Returns:
            Summary text
        """
        email = self.db.get_email(email_id)
        if not email:
            return "Email not found."
        
        query = f"Please provide a concise summary of this email in 2-3 sentences."
        email_context = self._build_email_context(email)
        
        response = self.llm.answer_query(query=query, email_context=email_context)
        return response or "Unable to generate summary."
    
    def extract_tasks_from_email(self, email_id: int) -> str:
        """
        Extract and format tasks from an email.
        
        Args:
            email_id: Email to extract tasks from
            
        Returns:
            Formatted task list
        """
        email = self.db.get_email(email_id)
        if not email:
            return "Email not found."
        
        if email.action_items and len(email.action_items) > 0:
            # Format existing action items
            tasks = []
            for i, item in enumerate(email.action_items, 1):
                task_str = f"{i}. {item.get('task', 'Unknown task')}"
                if item.get('deadline'):
                    task_str += f" (Due: {item['deadline']})"
                if item.get('priority'):
                    task_str += f" [Priority: {item['priority']}]"
                tasks.append(task_str)
            
            return "📋 **Action Items:**\n" + "\n".join(tasks)
        else:
            return "No action items found in this email."
    
    def search_inbox(self, query: str) -> str:
        """
        Search inbox and return formatted results.
        
        Args:
            query: Search query
            
        Returns:
            Formatted search results
        """
        emails = self.db.search_emails(query=query)
        
        if not emails:
            return f"No emails found matching '{query}'."
        
        results = [f"Found {len(emails)} email(s):\n"]
        for email in emails[:10]:  # Limit to 10 results
            results.append(f"- **{email.subject}** from {email.sender} [{email.category or 'Uncategorized'}]")
        
        if len(emails) > 10:
            results.append(f"\n... and {len(emails) - 10} more")
        
        return "\n".join(results)
    
    def get_urgent_emails(self) -> str:
        """
        Get list of urgent/important emails.
        
        Returns:
            Formatted list of urgent emails
        """
        emails = self.db.search_emails(category="Important")
        todo_emails = self.db.search_emails(category="To-Do")
        
        urgent = emails + todo_emails
        
        if not urgent:
            return "📭 No urgent emails at the moment!"
        
        results = [f"🚨 **{len(urgent)} Urgent/Important Email(s):**\n"]
        for email in urgent[:15]:
            indicator = "❗" if email.category == "Important" else "✅"
            results.append(f"{indicator} **{email.subject}** from {email.sender}")
        
        return "\n".join(results)
    
    def _build_email_context(self, email: Email) -> str:
        """
        Build context string for a single email.
        
        Args:
            email: Email object
            
        Returns:
            Formatted context string
        """
        context_parts = [
            f"Email ID: {email.id}",
            f"From: {email.sender}",
            f"Subject: {email.subject}",
            f"Date: {email.timestamp}",
            f"Category: {email.category or 'Uncategorized'}",
            f"\nContent:\n{email.body}"
        ]
        
        if email.action_items:
            context_parts.append(f"\nAction Items: {len(email.action_items)}")
            for item in email.action_items:
                context_parts.append(f"  - {item.get('task', 'Unknown')}")
        
        return "\n".join(context_parts)
    
    def _build_inbox_context(self, query: str) -> str:
        """
        Build context for inbox-wide queries.
        
        Args:
            query: User query to determine what context to gather
            
        Returns:
            Formatted context string
        """
        # Get summary statistics
        all_emails = self.db.get_all_emails()
        
        if not all_emails:
            return "Inbox is empty."
        
        # Category breakdown
        categories = {}
        total_actions = 0
        
        for email in all_emails:
            cat = email.category or "Uncategorized"
            categories[cat] = categories.get(cat, 0) + 1
            total_actions += len(email.action_items)
        
        context_parts = [
            f"Total Emails: {len(all_emails)}",
            f"Categories: {', '.join(f'{k}: {v}' for k, v in categories.items())}",
            f"Total Action Items: {total_actions}",
            "\nRecent Emails:"
        ]
        
        # Add recent emails
        for email in all_emails[:5]:
            context_parts.append(
                f"  - [{email.category or 'N/A'}] {email.subject} from {email.sender}"
            )
        
        return "\n".join(context_parts)
    
    def _is_inbox_query(self, query: str) -> bool:
        """
        Determine if query is inbox-wide (vs single email).
        
        Args:
            query: User query
            
        Returns:
            True if inbox-wide query
        """
        inbox_keywords = [
            "show", "list", "urgent", "important", "all",
            "how many", "what", "tasks", "emails from"
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in inbox_keywords)


# Singleton agent instance
email_agent = EmailAgent()
