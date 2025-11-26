"""Inbox viewer component for Streamlit UI."""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional

from backend.models import Email


def get_relative_time(timestamp: datetime) -> str:
    """Convert timestamp to relative time string."""
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    
    now = datetime.now(timestamp.tzinfo) if timestamp.tzinfo else datetime.utcnow()
    diff = now - timestamp
    
    if diff < timedelta(minutes=1):
        return "Just now"
    elif diff < timedelta(hours=1):
        mins = int(diff.total_seconds() / 60)
        return f"{mins} minute{'s' if mins != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(days=7):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return timestamp.strftime("%b %d, %Y")


def get_category_badge(category: Optional[str]) -> str:
    """Get colored badge HTML for category."""
    if not category:
        return "🔘 Uncategorized"
    
    badges = {
        "Important": "🔴 Important",
        "To-Do": "🟠 To-Do",
        "Newsletter": "🔵 Newsletter",
        "Spam": "⚫ Spam"
    }
    return badges.get(category, f"🔘 {category}")


def render_inbox_viewer(emails: list[Email], selected_email_id: Optional[int] = None):
    """
    Render email inbox viewer with filtering and search.
    
    Args:
        emails: List of Email objects to display
        selected_email_id: Currently selected email ID
    """
    st.markdown("### Inbox")
    
    # Search bar with better styling
    search_query = st.text_input(
        "Search",
        placeholder="Search emails by subject, sender, or content...",
        key="inbox_search",
        label_visibility="collapsed"
    )
    
    # Filters in expandable section
    with st.expander("Filters & Sorting", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            categories = ["All"] + sorted(list(set(e.category for e in emails if e.category)))
            selected_category = st.selectbox("Category", categories, key="category_filter")
        
        with col2:
            status_filter = st.selectbox("Status", ["All", "Processed", "Unprocessed"], key="status_filter")
        
        # Sort options in same expander
        sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Sender", "Category"], key="sort_by")
    
    # Filter emails
    filtered_emails = emails
    
    if search_query:
        filtered_emails = [
            e for e in filtered_emails
            if search_query.lower() in e.subject.lower()
            or search_query.lower() in e.sender.lower()
            or search_query.lower() in e.body.lower()
        ]
    
    if selected_category != "All":
        filtered_emails = [e for e in filtered_emails if e.category == selected_category]
    
    if status_filter == "Processed":
        filtered_emails = [e for e in filtered_emails if e.processed]
    elif status_filter == "Unprocessed":
        filtered_emails = [e for e in filtered_emails if not e.processed]
    
    # Sort emails
    if sort_by == "Date (Newest)":
        filtered_emails.sort(key=lambda x: x.timestamp, reverse=True)
    elif sort_by == "Date (Oldest)":
        filtered_emails.sort(key=lambda x: x.timestamp)
    elif sort_by == "Sender":
        filtered_emails.sort(key=lambda x: x.sender)
    elif sort_by == "Category":
        filtered_emails.sort(key=lambda x: x.category or "zzz")
    
    # Display count and bulk actions
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption(f"Showing **{len(filtered_emails)}** of **{len(emails)}** emails")
    with col2:
        if filtered_emails:
            unprocessed = [e for e in filtered_emails if not e.processed]
            if unprocessed and st.button("Process All", key="process_all_btn", use_container_width=True):
                st.session_state.process_batch = [e.id for e in unprocessed]
    
    st.divider()
    
    # Email list with modern card design
    if not filtered_emails:
        st.info("No emails match your filters. Try adjusting your search criteria.")
    else:
        # Container for scrollable email list
        for email in filtered_emails:
            # Email card with better styling
            is_selected = email.id == selected_email_id
            
            # Create a more compact, modern email card
            with st.container():
                # Main button for email selection
                status_indicator = "✓" if email.processed else "•"
                button_label = f"{status_indicator} {email.subject[:45]}..."
                
                if st.button(
                    button_label,
                    key=f"email_{email.id}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                    help=f"From: {email.sender}"
                ):
                    st.session_state.selected_email_id = email.id
                    st.rerun()
                
                # Metadata row
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.caption(f"From: {email.sender[:30]}")
                with col2:
                    st.caption(get_category_badge(email.category))
                with col3:
                    st.caption(get_relative_time(email.timestamp))
                
                # Action items indicator
                if email.action_items and len(email.action_items) > 0:
                    st.caption(f"{len(email.action_items)} task{'s' if len(email.action_items) > 1 else ''}")
                
                st.markdown("<br>", unsafe_allow_html=True)


def render_email_detail(email: Email):
    """
    Render detailed view of selected email.
    
    Args:
        email: Email object to display
    """
    # Modern header with status badge
    status_text = "Processed" if email.processed else "Unprocessed"
    st.markdown(f"### Email Details ({status_text})")
    
    # Email metadata card
    with st.container():
        st.markdown(f"## {email.subject}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**From:** {email.sender}")
            st.caption(f"Received: {get_relative_time(email.timestamp)}")
        with col2:
            if email.category:
                st.markdown("**Category:**")
                st.markdown(get_category_badge(email.category))
    
    # Action button
    if not email.processed:
        if st.button("Process Email", key="process_single", use_container_width=True, type="primary"):
            st.session_state.process_email_id = email.id
            st.rerun()
    else:
        st.success("Email has been processed")
    
    st.divider()
    
    # Email body with better presentation
    st.markdown("### Message")
    with st.container():
        # Use a box for better visual separation
        st.markdown(f"""
            <div style='
                background-color: rgba(240, 242, 246, 0.5);
                padding: 1.5rem;
                border-radius: 8px;
                border-left: 4px solid #6366f1;
                max-height: 400px;
                overflow-y: auto;
            '>
                {email.body.replace(chr(10), '<br>')}
            </div>
        """, unsafe_allow_html=True)
    
    # Action items with modern design
    if email.action_items and len(email.action_items) > 0:
        st.divider()
        st.markdown("### Action Items")
        
        for i, item in enumerate(email.action_items, 1):
            # Handle both dict and string cases
            if isinstance(item, str):
                # If item is a string, display it directly
                with st.expander(f"**Task {i}:** {item[:45]}...", expanded=i==1):
                    st.markdown(f"**Task:** {item}")
            elif isinstance(item, dict):
                # If item is a dict, use the normal structure
                task_title = item.get('task', 'Unknown')[:45]
                with st.expander(f"**Task {i}:** {task_title}...", expanded=i==1):
                    st.markdown(f"**Task:** {item.get('task', 'Unknown')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if item.get('deadline'):
                            st.markdown(f"**Deadline:** {item.get('deadline')}")
                    with col2:
                        if item.get('priority'):
                            priority = item.get('priority', '').lower()
                            priority_emoji = {
                                'high': '🔴',
                                'medium': '🟡',
                                'low': '🟢'
                            }.get(priority, '⚪')
                            priority_label = item.get('priority').title()
                            st.markdown(f"**Priority:** {priority_emoji} {priority_label}")
            else:
                # Fallback for unexpected types
                with st.expander(f"**Task {i}:** [Invalid format]", expanded=False):
                    st.warning(f"Unable to parse action item: {str(item)}")
    
    # Quick actions with modern button styling
    st.divider()
    st.markdown("### Quick Actions")
    st.caption("Use AI to interact with this email")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Summarize", key="summarize_btn", use_container_width=True, help="Get a concise summary"):
            st.session_state.quick_action = ("summarize", email.id)
    
    with col2:
        if st.button("Draft Reply", key="draft_btn", use_container_width=True, help="Generate a reply draft"):
            st.session_state.quick_action = ("draft", email.id)
    
    with col3:
        if st.button("Extract Tasks", key="extract_btn", use_container_width=True, help="Find action items"):
            st.session_state.quick_action = ("extract_tasks", email.id)
