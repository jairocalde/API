# src/services/validation_service.py
import re
from typing import Tuple, Optional
from datetime import datetime

class ValidationService:
    INAPPROPRIATE_WORDS = ["malapalabra", "inapropiado", "ofensivo", "prohibido"]

    def validate_message_format(self, message_data: dict) -> Tuple[bool, Optional[str]]:
        required_fields = ["message_id", "session_id", "content", "timestamp", "sender"]

        for field in required_fields:
            if field not in message_data or not message_data[field]:
                return False, f"Campo requerido faltante: '{field}'"

        if message_data["sender"] not in ["user", "system"]:
            return False, "El campo 'sender' debe ser 'user' o 'system'"

        if not re.match(r'^[a-zA-Z0-9\-_]+$', message_data["message_id"]):
            return False, "message_id solo puede contener letras, números, guiones y guiones bajos"

        return True, None

    def validate_content(self, content: str) -> Tuple[bool, Optional[str]]:
        if not content or not content.strip():
            return False, "El contenido no puede estar vacío"

        if len(content.strip()) > 1000:
            return False, "El contenido no puede exceder 1000 caracteres"

        content_lower = content.lower()
        for word in self.INAPPROPRIATE_WORDS:
            if word in content_lower:
                return False, "El contenido contiene palabras inapropiadas"

        return True, None

    def validate_timestamp(self, timestamp: datetime) -> Tuple[bool, Optional[str]]:
        now = datetime.now(timestamp.tzinfo)
        if timestamp > now:
            return False, "El timestamp no puede ser una fecha futura"
        return True, None
