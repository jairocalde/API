# src/services/message_service.py
from typing import Dict, Optional
from datetime import datetime

class MessageService:
    def __init__(self, repository):
        self.repository = repository
        
        # Importar aquí para evitar problemas circulares
        from .validation_service import ValidationService
        from .processing_pipeline import ProcessingPipeline
        
        self.validator = ValidationService()
        self.processor = ProcessingPipeline()
    
    def create_message(self, message_data: dict) -> Dict:
        # Validar formato del mensaje
        is_valid, error_message = self.validator.validate_message_format(message_data)
        if not is_valid:
            raise ValueError(error_message)
        
        # Validar contenido
        is_valid_content, content_error = self.validator.validate_content(message_data["content"])
        if not is_valid_content:
            raise ValueError(content_error)
        
        # Validar timestamp usando el servicio de validación
        is_valid_time, time_error, timestamp = self.validator.validate_timestamp(message_data["timestamp"])
        if not is_valid_time:
            raise ValueError(time_error)
        
        # Verificar si el mensaje ya existe
        if self.repository.message_exists(message_data["message_id"]):
            raise ValueError(f"El mensaje con ID '{message_data['message_id']}' ya existe")
        
        # Procesar mensaje
        metadata = self.processor.process_message(message_data["content"])
        
        # Aquí normalmente guardaríamos en la base de datos
        # Por ahora simulamos la respuesta
        
        return {
            "message_id": message_data["message_id"],
            "session_id": message_data["session_id"],
            "content": metadata["filtered_content"],
            "timestamp": message_data["timestamp"],
            "sender": message_data["sender"],
            "metadata": {
                "word_count": metadata["word_count"],
                "character_count": metadata["character_count"],
                "processed_at": metadata["processed_at"].isoformat(),
                "is_filtered": metadata["is_filtered"]
            }
        }
    
    def get_messages_by_session(
        self, 
        session_id: str, 
        skip: int = 0, 
        limit: int = 100, 
        sender: Optional[str] = None
    ) -> Dict:
        # Por ahora retornamos datos simulados
        return {
            "session_id": session_id,
            "messages": [],
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": 0,
                "has_more": False
            }
        }