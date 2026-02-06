# src/services/processing_pipeline.py
from datetime import datetime

def process_message_content(content: str) -> dict:
    return {
        "word_count": len(content.split()),
        "character_count": len(content),
        "processed_at": datetime.utcnow().isoformat() + "Z"
    }
