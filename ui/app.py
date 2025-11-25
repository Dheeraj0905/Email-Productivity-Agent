"""Main Streamlit application for Email Productivity Agent."""
import streamlit as st
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import config
from backend.database import db
from backend.email_processor import email_processor
from backend.agent_logic import email_agent
from ui.components.inbox_viewer import render_inbox_viewer, render_email_detail
from ui.components.prompt_editor import render_prompt_editor
from ui.components.agent_chat import render_agent_chat
from ui.components.draft_manager import render_draft_manager


# Page configuration
st.set_page_config(
    page_title="Email Productivity Agent",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_app():
    """Initialize application state and database."""
    # Validate configuration
    is_valid, error_msg = config.validate()
    if not is_valid:
        st.error(f"⚠️ Configuration Error: {error_msg}")
        st.info("💡 Please add your OpenAI API key to the `.env` file")
        st.stop()
    
    # Initialize database
    try:
        db.init_database()
    except Exception as e:
        st.error(f"❌ Database initialization failed: {e}")
        st.stop()
    
    # Initialize session state
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.selected_email_id = None
        st.session_state.emails_loaded = False
        st.session_state.chat_history = []
        st.session_state.view_mode = "inbox"  # inbox, drafts
        st.session_state.quick_action = None
        st.session_state.process_email_id = None
        st.session_state.process_batch = None


def load_emails():
    """Load emails from database or mock data."""
    emails = db.get_all_emails()
    
    if not emails:
        # Load mock inbox
        with st.spinner("📥 Loading mock inbox..."):
            count = email_processor.load_mock_inbox()
            if count > 0:
                st.success(f"✓ Loaded {count} emails from mock inbox")
                emails = db.get_all_emails()
            else:
                st.warning("⚠️ No emails found. Check if mock_inbox.json exists in data/ folder.")
    
    return emails


def process_email_action(email_id: int):
    """Process a single email."""
    with st.spinner(f"🔄 Processing email {email_id}..."):
        success = email_processor.process_email(email_id)
        if success:
            st.success(f"✓ Email {email_id} processed successfully!")
        else:
            st.error(f"❌ Failed to process email {email_id}")
    st.session_state.process_email_id = None


def process_batch_emails(email_ids: list):
    """Process multiple emails in batch."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = {"total": len(email_ids), "successful": 0, "failed": 0}
    
    for i, email_id in enumerate(email_ids):
        status_text.text(f"Processing email {i+1}/{len(email_ids)}...")
        success = email_processor.process_email(email_id)
        
        if success:
            results["successful"] += 1
        else:
            results["failed"] += 1
        
        progress_bar.progress((i + 1) / len(email_ids))
    
    status_text.empty()
    progress_bar.empty()
    
    st.success(f"✓ Batch processing complete: {results['successful']}/{results['total']} successful")
    st.session_state.process_batch = None


def main():
    """Main application entry point."""
    # Initialize
    initialize_app()
    
    # Modern Header with gradient-like styling
    st.markdown("""
        <style>
        .main-header {
            padding: 1.5rem 0;
            background: linear-gradient(90deg, rgba(99,102,241,0.1) 0%, rgba(168,85,247,0.1) 100%);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .stButton > button {
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        div[data-testid="stExpander"] {
            border-radius: 8px;
            border: 1px solid #e5e7eb;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.markdown("# 📧 Email Productivity Agent")
        st.caption("AI-Powered Email Management & Automation")
    with col2:
        st.markdown("")  # Spacer
        st.markdown("")  # Spacer
        # Show LLM provider badge
        provider = config.LLM_PROVIDER.upper()
        if provider == "OLLAMA":
            st.success(f"**Using:** {provider} ")
        else:
            st.info(f"**Using:** {provider}")
    with col3:
        st.markdown("")  # Spacer
        st.markdown("")  # Spacer
        # View mode selector
        view = st.selectbox(
            "📂 View Mode",
            ["📥 Inbox", "✉️ Drafts"],
            key="view_selector",
        )
        st.session_state.view_mode = "drafts" if "Drafts" in view else "inbox"
    
    st.divider()
    
    # Modern Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings & Controls")
        
        # Reload button at top
        if st.button("🔄 Reload Data", use_container_width=True, type="primary"):
            st.rerun()
        
        st.divider()
        
        # Prompt Brain Editor
        render_prompt_editor()
        
        st.divider()
        
        # System Stats - Modern Card Style
        st.markdown("### 📊 System Statistics")
        
        emails = load_emails()
        processed_count = sum(1 for e in emails if e.processed)
        unprocessed_count = len(emails) - processed_count
        
        # Stats cards
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", len(emails))
            st.metric("✅ Processed", processed_count)
        with col2:
            st.metric("📥 Inbox", unprocessed_count)
            processing_rate = (processed_count / len(emails) * 100) if emails else 0
            st.metric("📈 Rate", f"{processing_rate:.0f}%")
        
        # Token usage (if available)
        from backend.unified_llm_service import unified_llm_service
        tokens = unified_llm_service.get_token_usage()
        if tokens > 0:
            st.divider()
            st.metric("AI Requests", f"{tokens:,}")
        
        # Model info
        st.divider()
        st.caption(f"**Model:** {config.OPENAI_MODEL if config.LLM_PROVIDER == 'openai' else config.OLLAMA_MODEL}")
        st.caption(f"**Version:** {config.APP_VERSION}")
    
    # Main content area - Modern Three-Column Layout
    if st.session_state.view_mode == "inbox":
        col_left, col_center, col_right = st.columns([2.5, 3.5, 3], gap="large")
        
        # Left: Email List
        with col_left:
            with st.container():
                render_inbox_viewer(emails, st.session_state.selected_email_id)
        
        # Center: Email Detail
        with col_center:
            with st.container():
                if st.session_state.selected_email_id:
                    email = db.get_email(st.session_state.selected_email_id)
                    if email:
                        render_email_detail(email)
                    else:
                        st.info("Select an email from the inbox to view details")
                else:
                    # Welcome screen with stats
                    st.markdown("### Welcome to Your Inbox")
                    st.info("Select an email from the list to get started")
                    
                    st.divider()
                    
                    # Quick insights dashboard
                    st.markdown("### Inbox Insights")
                    
                    # Category breakdown with visual appeal
                    categories = {}
                    for email in emails:
                        cat = email.category or "Uncategorized"
                        categories[cat] = categories.get(cat, 0) + 1
                    
                    if categories:
                        st.markdown("#### 📁 By Category")
                        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                            percentage = (count / len(emails) * 100) if emails else 0
                            st.progress(percentage / 100)
                            st.caption(f"**{cat}:** {count} emails ({percentage:.0f}%)")
                            st.markdown("")
                    
                    # Action items summary
                    total_actions = sum(len(e.action_items) for e in emails)
                    st.divider()
                    st.markdown("#### ✅ Action Items")
                    st.metric("Total Tasks", total_actions)
                    
                    # Recent activity
                    st.divider()
                    st.markdown("#### 🕐 Recent Activity")
                    recent_processed = [e for e in emails if e.processed][-5:]
                    if recent_processed:
                        for email in reversed(recent_processed):
                            st.caption(f"✅ {email.subject[:40]}...")
                    else:
                        st.caption("No processed emails yet")
        
        # Right: Agent Chat
        with col_right:
            with st.container():
                render_agent_chat(st.session_state.selected_email_id)
    
    else:
        # Drafts view - Clean two-column layout
        col_left, col_right = st.columns([1, 1], gap="large")
        
        with col_left:
            with st.container():
                render_draft_manager(st.session_state.selected_email_id)
        
        with col_right:
            with st.container():
                render_agent_chat(st.session_state.selected_email_id)
    
    # Handle processing actions
    if st.session_state.process_email_id:
        process_email_action(st.session_state.process_email_id)
        st.rerun()
    
    if st.session_state.process_batch:
        process_batch_emails(st.session_state.process_batch)
        st.rerun()
    
    # Handle quick actions
    if st.session_state.quick_action:
        action_type, email_id = st.session_state.quick_action
        st.session_state.quick_action = None
        
        if action_type == "summarize":
            st.session_state.pending_query = "Summarize this email"
        elif action_type == "draft":
            st.session_state.pending_query = "Draft a reply to this email"
        elif action_type == "extract_tasks":
            st.session_state.pending_query = "Extract action items from this email"
        
        st.rerun()
    
    # Modern Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0; color: #6b7280;'>
            <p style='margin: 0.5rem 0;'>
                <strong>⚠️ Important:</strong> All drafts are for review only - NOT sent automatically
            </p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
                Built with ❤️ using Streamlit• 
                <strong>Model:</strong> {model} • 
                <strong>Version:</strong> {version}
            </p>
        </div>
    """.format(
        model=config.OPENAI_MODEL if config.LLM_PROVIDER == 'openai' else config.OLLAMA_MODEL,
        version=config.APP_VERSION
    ), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
