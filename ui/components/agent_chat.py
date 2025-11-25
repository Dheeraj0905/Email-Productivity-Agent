"""Agent chat component for Streamlit UI."""
import streamlit as st
from typing import Optional
from datetime import datetime

from backend.agent_logic import email_agent
from backend.models import AgentMessage


def render_agent_chat(selected_email_id: Optional[int] = None):
    """
    Render chat interface with the email agent.
    
    Args:
        selected_email_id: Currently selected email for context
    """
    st.markdown("### 💬 AI Assistant")
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Context indicator with modern styling
    if selected_email_id:
        from backend.database import db
        email = db.get_email(selected_email_id)
        if email:
            st.success(f"💌 **Context:** {email.subject[:50]}...", icon="🎯")
    else:
        st.info("💬 **General Mode** - Ask about your inbox", icon="📬")
    
    # Quick action buttons with better organization
    with st.expander("⚡ Quick Actions", expanded=True):
        st.caption("Click a button to start a conversation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Summarize", key="chat_summarize", use_container_width=True, disabled=not selected_email_id):
                query = "Summarize this email"
                st.session_state.pending_query = query
            
            if st.button("✉️ Draft Reply", key="chat_draft", use_container_width=True, disabled=not selected_email_id):
                query = "Draft a reply to this email"
                st.session_state.pending_query = query
        
        with col2:
            if st.button("📋 Extract Tasks", key="chat_extract", use_container_width=True, disabled=not selected_email_id):
                query = "Extract action items from this email"
                st.session_state.pending_query = query
            
            if st.button("🚨 Show Urgent", key="chat_urgent", use_container_width=True):
                query = "Show me urgent emails"
                st.session_state.pending_query = query
    
    st.divider()
    
    # Chat history display with modern styling
    st.markdown("#### 💭 Conversation")
    chat_container = st.container(height=350)
    
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
                <div style='
                    text-align: center;
                    padding: 3rem 1rem;
                    color: #6b7280;
                '>
                    <h3>👋 Hello!</h3>
                    <p>I'm your AI email assistant. I can help you:</p>
                    <ul style='text-align: left; display: inline-block;'>
                        <li>📝 Summarize emails</li>
                        <li>✉️ Draft replies</li>
                        <li>📋 Extract action items</li>
                        <li>🔍 Search your inbox</li>
                        <li>📊 Analyze email patterns</li>
                    </ul>
                    <p><strong>Ask me anything!</strong></p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg.role == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(msg.content)
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(msg.content)
    
    # Process pending query (from quick actions)
    if "pending_query" in st.session_state and st.session_state.pending_query:
        query = st.session_state.pending_query
        st.session_state.pending_query = None
        
        # Add user message
        user_msg = AgentMessage(
            role="user",
            content=query,
            timestamp=datetime.utcnow()
        )
        st.session_state.chat_history.append(user_msg)
        
        # Get agent response
        with st.spinner("Thinking..."):
            response = email_agent.handle_query(
                user_query=query,
                selected_email_id=selected_email_id,
                conversation_history=st.session_state.chat_history[:-1]
            )
        
        # Add assistant message
        assistant_msg = AgentMessage(
            role="assistant",
            content=response,
            timestamp=datetime.utcnow()
        )
        st.session_state.chat_history.append(assistant_msg)
        st.rerun()
    
    # Chat input
    user_input = st.chat_input("Ask about your emails...", key="chat_input")
    
    if user_input:
        # Add user message
        user_msg = AgentMessage(
            role="user",
            content=user_input,
            timestamp=datetime.utcnow()
        )
        st.session_state.chat_history.append(user_msg)
        
        # Get agent response
        with st.spinner("Thinking..."):
            response = email_agent.handle_query(
                user_query=user_input,
                selected_email_id=selected_email_id,
                conversation_history=st.session_state.chat_history[:-1]
            )
        
        # Add assistant message
        assistant_msg = AgentMessage(
            role="assistant",
            content=response,
            timestamp=datetime.utcnow()
        )
        st.session_state.chat_history.append(assistant_msg)
        st.rerun()
    
    # Chat management buttons
    st.divider()
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.session_state.chat_history:
            chat_text = "\n\n".join([
                f"{'User' if msg.role == 'user' else 'Assistant'}: {msg.content}"
                for msg in st.session_state.chat_history
            ])
            st.download_button(
                "📥 Export",
                chat_text,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="download_chat",
                use_container_width=True
            )
        else:
            st.button("📥 Export", key="export_disabled", use_container_width=True, disabled=True)
