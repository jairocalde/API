from src.services.validation_service import ValidationService # Importa servicios de validación y procesamiento
from src.services.processing_pipeline import process_message_content 
from datetime import datetime # Importa datetime para manejo de fechas
from fastapi import HTTPException# Importa HTTPException para errores HTTP

class MessageService: # Clase principal de servicio - contiene la lógica de negocio

    def __init__(self, repository):  # Constructor que recibe el repositorio (inyección de dependencias)
        self.repository = repository
        self.validator = ValidationService()

    def process_message(self, message):   # Método principal: procesa un mensaje end-to-end
        # Validaciones
        is_valid, error = self.validator.validate_message_format(message.dict())  # Valida el formato del mensaje (campos requeridos)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)

        is_valid, error = self.validator.validate_content(message.content)  # Valida el contenido (no vacío, tipo string)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)

        is_valid, error = self.validator.validate_timestamp(message.timestamp)    # Valida el timestamp (formato ISO 8601)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error)

        metadata = process_message_content(message.content) # Procesa el contenido para extraer metadata

        data = { # Prepara el diccionario con todos los datos
            "message_id": message.message_id,
            "session_id": message.session_id,
            "content": message.content,
            "timestamp": message.timestamp,  # 👈 datetime, NO string
            "sender": message.sender,
            "message_metadata": metadata
        }

        try: # Guarda en base de datos a través del repositorio
            self.repository.save_message(data)
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))

        return data # Retorna los datos procesados
