"""Prompt editor component for Streamlit UI."""
import streamlit as st
from typing import Dict, Any
import json

from backend.database import db
from backend.models import Prompt
from datetime import datetime


def load_default_prompts() -> Dict[str, Any]:
    """Load default prompts from JSON file."""
    try:
        with open("prompts/default_prompts.json", 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading default prompts: {e}")
        return {}


def render_prompt_editor():
    """Render the Prompt Brain configuration panel."""
    st.sidebar.header("Prompt Brain")
    st.sidebar.caption("Configure how the agent processes emails")
    
    # Load current prompts from database
    current_prompts = {p.prompt_type: p for p in db.get_all_prompts()}
    default_prompts = load_default_prompts()
    
    # Categorization Prompt
    with st.sidebar.expander("Categorization Prompt", expanded=False):
        st.caption("How emails are categorized into Important, To-Do, Newsletter, or Spam")
        
        current_cat = current_prompts.get("categorization")
        default_cat = default_prompts.get("categorization", {}).get("prompt", "")
        
        cat_prompt = st.text_area(
            "Categorization Prompt",
            value=current_cat.prompt_text if current_cat else default_cat,
            height=200,
            key="cat_prompt",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", key="save_cat"):
                prompt = Prompt(
                    id=None,
                    prompt_type="categorization",
                    prompt_text=cat_prompt,
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.insert_prompt(prompt)
                st.success("✓ Saved!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_cat"):
                if default_cat:
                    prompt = Prompt(
                        id=None,
                        prompt_type="categorization",
                        prompt_text=default_cat,
                        is_active=True,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.insert_prompt(prompt)
                    st.success("✓ Reset to default!")
                    st.rerun()
    
    # Action Item Extraction Prompt
    with st.sidebar.expander("📋 Action Item Extraction", expanded=False):
        st.caption("How tasks are extracted from emails (returns JSON)")
        
        current_action = current_prompts.get("action_extraction")
        default_action = default_prompts.get("action_extraction", {}).get("prompt", "")
        
        action_prompt = st.text_area(
            "Action Extraction Prompt",
            value=current_action.prompt_text if current_action else default_action,
            height=200,
            key="action_prompt",
            label_visibility="collapsed"
        )
        
        st.info("💡 Response must be valid JSON array")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", key="save_action"):
                prompt = Prompt(
                    id=None,
                    prompt_type="action_extraction",
                    prompt_text=action_prompt,
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.insert_prompt(prompt)
                st.success("✓ Saved!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_action"):
                if default_action:
                    prompt = Prompt(
                        id=None,
                        prompt_type="action_extraction",
                        prompt_text=default_action,
                        is_active=True,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.insert_prompt(prompt)
                    st.success("✓ Reset to default!")
                    st.rerun()
    
    # Auto-Reply Draft Prompt
    with st.sidebar.expander("✉️ Auto-Reply Draft", expanded=False):
        st.caption("How draft replies are generated")
        
        current_reply = current_prompts.get("auto_reply")
        default_reply = default_prompts.get("auto_reply", {}).get("prompt", "")
        
        reply_prompt = st.text_area(
            "Auto-Reply Prompt",
            value=current_reply.prompt_text if current_reply else default_reply,
            height=200,
            key="reply_prompt",
            label_visibility="collapsed"
        )
        
        # Tone selector
        tone = st.selectbox(
            "Tone",
            ["Professional", "Friendly", "Casual"],
            key="reply_tone"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", key="save_reply"):
                # Add tone instruction to prompt
                final_prompt = reply_prompt
                if tone:
                    final_prompt += f"\n\nTone: {tone}"
                
                prompt = Prompt(
                    id=None,
                    prompt_type="auto_reply",
                    prompt_text=final_prompt,
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.insert_prompt(prompt)
                st.success("✓ Saved!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_reply"):
                if default_reply:
                    prompt = Prompt(
                        id=None,
                        prompt_type="auto_reply",
                        prompt_text=default_reply,
                        is_active=True,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.insert_prompt(prompt)
                    st.success("✓ Reset to default!")
                    st.rerun()
    
    # Prompt Statistics
    st.sidebar.divider()
    st.sidebar.caption("📊 **Prompt Statistics**")
    st.sidebar.caption(f"Active Prompts: {len(current_prompts)}/3")
    
    # Initialize prompts button
    if len(current_prompts) < 3:
        if st.sidebar.button("🔧 Initialize Default Prompts", use_container_width=True):
            for prompt_type, prompt_data in default_prompts.items():
                if prompt_type not in current_prompts:
                    prompt = Prompt(
                        id=None,
                        prompt_type=prompt_type,
                        prompt_text=prompt_data["prompt"],
                        is_active=True,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.insert_prompt(prompt)
            st.success("✓ Default prompts initialized!")
            st.rerun()
