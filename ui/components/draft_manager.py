"""Draft manager component for Streamlit UI."""
import streamlit as st
from datetime import datetime
from typing import Optional

from backend.database import db
from backend.agent_logic import email_agent
from backend.models import Draft


def render_draft_manager(selected_email_id: Optional[int] = None):
    """
    Render draft email manager.
    
    Args:
        selected_email_id: Currently selected email ID
    """
    st.subheader("✉️ Draft Manager")
    
    # Get drafts for selected email or all drafts
    if selected_email_id:
        drafts = db.get_drafts(email_id=selected_email_id)
        st.caption(f"Drafts for current email ({len(drafts)})")
    else:
        drafts = db.get_drafts()
        st.caption(f"All drafts ({len(drafts)})")
    
    # Warning banner
    st.warning("⚠️ **These are DRAFTS.** They will NOT be sent automatically. Review carefully before using.")
    
    st.divider()
    
    # Generate new draft button
    if selected_email_id:
        col1, col2 = st.columns([2, 1])
        with col1:
            user_instruction = st.text_input(
                "Custom instructions (optional)",
                placeholder="e.g., 'Be more formal' or 'Ask for more details'",
                key="draft_instruction"
            )
        with col2:
            if st.button("Generate Draft", key="generate_draft", use_container_width=True):
                with st.spinner("Generating draft..."):
                    draft = email_agent.generate_draft(
                        email_id=selected_email_id,
                        user_instruction=user_instruction if user_instruction else None
                    )
                    if draft:
                        st.success("✓ Draft created!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to generate draft")
        
        st.divider()
    
    # Display drafts
    if not drafts:
        st.info("📭 No drafts yet. Generate a draft for an email to get started!")
    else:
        for draft in drafts:
            with st.expander(f"📄 Draft #{draft.id} - {draft.subject}", expanded=len(drafts) == 1):
                # Draft metadata
                st.caption(f"**Created:** {draft.created_at.strftime('%Y-%m-%d %H:%M')}")
                
                if draft.metadata.get("original_sender"):
                    st.caption(f"**Original Email From:** {draft.metadata['original_sender']}")
                
                if draft.metadata.get("user_instruction"):
                    st.caption(f"**Custom Instructions:** {draft.metadata['user_instruction']}")
                
                st.divider()
                
                # Editable subject
                edited_subject = st.text_input(
                    "Subject",
                    value=draft.subject,
                    key=f"draft_subject_{draft.id}"
                )
                
                # Editable body
                edited_body = st.text_area(
                    "Body",
                    value=draft.body,
                    height=250,
                    key=f"draft_body_{draft.id}"
                )
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📋 Copy", key=f"copy_{draft.id}", use_container_width=True):
                        # Note: Actual clipboard copy requires additional library
                        st.info("💡 Copy the text manually from the text area above")
                
                with col2:
                    if st.button("🔄 Regenerate", key=f"regen_{draft.id}", use_container_width=True):
                        with st.spinner("✍️ Regenerating..."):
                            new_draft = email_agent.generate_draft(
                                email_id=draft.email_id,
                                user_instruction="Rewrite the previous draft with a different approach"
                            )
                            if new_draft:
                                st.success("✓ New draft created!")
                                st.rerun()
                
                with col3:
                    # Download draft button
                    draft_content = f"Subject: {edited_subject}\n\n{edited_body}"
                    st.download_button(
                        "💾 Download",
                        draft_content,
                        file_name=f"draft_{draft.id}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        key=f"download_{draft.id}",
                        use_container_width=True
                    )
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{draft.id}", use_container_width=True, type="secondary"):
                        db.delete_draft(draft.id)
                        st.success("✓ Draft deleted")
                        st.rerun()
                
                st.divider()
                
                # Original email reference
                if draft.email_id:
                    with st.expander("📧 View Original Email"):
                        original_email = db.get_email(draft.email_id)
                        if original_email:
                            st.markdown(f"**From:** {original_email.sender}")
                            st.markdown(f"**Subject:** {original_email.subject}")
                            st.markdown(f"**Body:**")
                            st.text_area(
                                "Original",
                                value=original_email.body,
                                height=150,
                                disabled=True,
                                key=f"original_{draft.id}",
                                label_visibility="collapsed"
                            )


def render_draft_history():
    """Render draft history view."""
    st.subheader("📚 Draft History")
    
    drafts = db.get_drafts()
    
    if not drafts:
        st.info("No drafts in history.")
        return
    
    # Group by email
    drafts_by_email = {}
    for draft in drafts:
        if draft.email_id not in drafts_by_email:
            drafts_by_email[draft.email_id] = []
        drafts_by_email[draft.email_id].append(draft)
    
    for email_id, email_drafts in drafts_by_email.items():
        email = db.get_email(email_id)
        email_subject = email.subject if email else f"Email #{email_id}"
        
        with st.expander(f"📧 {email_subject} ({len(email_drafts)} drafts)"):
            for draft in email_drafts:
                st.markdown(f"**Draft #{draft.id}** - {draft.created_at.strftime('%Y-%m-%d %H:%M')}")
                st.caption(draft.subject)
                st.divider()
