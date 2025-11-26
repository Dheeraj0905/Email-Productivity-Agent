"""Initialize default prompts in database."""
import json
import logging
from datetime import datetime

from backend.database import db
from backend.models import Prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_default_prompts():
    """Load default prompts from JSON file into database."""
    try:
        # Load prompts from JSON
        with open("prompts/default_prompts.json", 'r') as f:
            default_prompts = json.load(f)
        
        logger.info(f"Loaded {len(default_prompts)} prompt templates from JSON")
        
        # Check which prompts already exist
        existing_prompts = {p.prompt_type: p for p in db.get_all_prompts()}
        logger.info(f"Found {len(existing_prompts)} prompts already in database")
        
        # Insert missing prompts
        added_count = 0
        for prompt_type, prompt_data in default_prompts.items():
            if prompt_type not in existing_prompts:
                prompt = Prompt(
                    id=None,
                    prompt_type=prompt_type,
                    prompt_text=prompt_data["prompt"],
                    is_active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.insert_prompt(prompt)
                added_count += 1
                logger.info(f"✓ Added prompt: {prompt_type}")
            else:
                logger.info(f"- Prompt already exists: {prompt_type}")
        
        if added_count > 0:
            logger.info(f"\n✓ Successfully added {added_count} prompts to database!")
        else:
            logger.info("\n✓ All prompts already exist in database!")
        
        # Verify final count
        all_prompts = db.get_all_prompts()
        logger.info(f"\nTotal prompts in database: {len(all_prompts)}")
        for p in all_prompts:
            logger.info(f"  - {p.prompt_type}: {len(p.prompt_text)} characters")
        
        return True
        
    except FileNotFoundError:
        logger.error("prompts/default_prompts.json not found!")
        return False
    except Exception as e:
        logger.error(f"Error loading prompts: {e}")
        return False


if __name__ == "__main__":
    logger.info("Initializing database...")
    db.init_database()
    
    logger.info("\nLoading default prompts...")
    success = load_default_prompts()
    
    if success:
        print("\n" + "="*50)
        print("✓ Prompts initialized successfully!")
        print("="*50)
        print("\nYou can now:")
        print("1. Run the app: streamlit run ui/app.py")
        print("2. Click 'Process Email' to categorize emails")
        print("3. View prompts in the sidebar 'Prompt Brain'")
    else:
        print("\n" + "="*50)
        print("✗ Failed to initialize prompts")
        print("="*50)
        print("\nPlease check the error messages above")
