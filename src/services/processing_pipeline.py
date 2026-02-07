# src/services/processing_pipeline.py
from datetime import datetime # Importa datetime para timestamp de procesamiento

def process_message_content(content: str) -> dict: # Función que procesa el contenido de un mensaje y extrae metadata
    return {
        "word_count": len(content.split()), # Número de palabras (split por espacios)
        "character_count": len(content), # Número total de caracteres
        "processed_at": datetime.utcnow().isoformat() + "Z" # Timestamp UTC en ISO con Z
    }
