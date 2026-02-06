# src/services/message_service.py
from src.services.validation_service import ValidationService
from src.services.processing_pipeline import process_message_content

class MessageService:

    def __init__(self, repository):
        self.repository = repository
        self.validator = ValidationService()

    def process_message(self, message):
        is_valid, error = self.validator.validate_message_format(message.dict())
        if not is_valid:
            raise ValueError(error)

        is_valid, error = self.validator.validate_content(message.content)
        if not is_valid:
            raise ValueError(error)

        is_valid, error = self.validator.validate_timestamp(message.timestamp)
        if not is_valid:
            raise ValueError(error)

        metadata = process_message_content(message.content)

        data = {
            "message_id": message.message_id,
            "session_id": message.session_id,
            "content": message.content,
            "timestamp": message.timestamp.isoformat().replace("+00:00", "Z"),
            "sender": message.sender,
            "metadata": metadata
        }

        # Guardar usando el repositorio
        self.repository.save_message(data)

        return data
