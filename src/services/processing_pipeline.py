# src/services/processing_pipeline.py
from typing import Dict
import datetime

# REQUERIMIENTO 3. Pipeline de procesamiento simple

class ProcessingPipeline:
    def __init__(self):
        self.inappropriate_words = ["malapalabra", "inapropiado", "prohibido"]
    
    def process_message(self, content: str) -> Dict:
        """Procesa el mensaje y genera metadatos
          
        REQUERIMIENTO: 3. Pipeline de procesamiento simple que:
        1. Valide el formato del mensaje (colabora con ValidationService)
        2. Verifique y filtre contenido inapropiado
        3. Agregue metadatos (longitud del mensaje, conteo de palabras)
        """
        
        # Contar palabras y caracteres
        words = content.split()
        word_count = len(words)
        character_count = len(content)
        
        # Verificar contenido inapropiado
        is_filtered = self._contains_inappropriate_content(content)
        
        # Aplicar filtrado (reemplazar palabras inapropiadas)
        if is_filtered:
            filtered_content = self._filter_content(content)
        else:
            filtered_content = content
        
        return {
            "word_count": word_count,
            "character_count": character_count,
            "processed_at": datetime.datetime.now(),
            "is_filtered": is_filtered,
            "filtered_content": filtered_content
        }
    
    def _contains_inappropriate_content(self, content: str) -> bool:
        """Verifica si el contenido contiene palabras inapropiadas"""
        content_lower = content.lower()
        for word in self.inappropriate_words:
            if word in content_lower:
                return True
        return False
    
    def _filter_content(self, content: str) -> str:
        """Filtra palabras inapropiadas (implementación simple)"""
        filtered_content = content
        for word in self.inappropriate_words:
            filtered_content = filtered_content.lower().replace(word, "***")
        return filtered_content