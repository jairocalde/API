# src/services/validation_service.py
import re
from typing import Tuple, Optional
from datetime import datetime

# REQUERIMIENTOS: 1.2 y 3.1 - Servicio de Validación de Mensajes

class ValidationService:
    # Lista simple de palabras inapropiadas
    """REQ: 1.2. Valida los mensajes entrantes
        REQ: 3.1. Valide el formato del mensaje (parte del pipeline)
        REQ: 5. Manejo de errores - Validación de formato y campos
    """

    INAPPROPRIATE_WORDS = ["malapalabra", "inapropiado", "ofensivo", "prohibido"]
    
    def validate_message_format(self, message_data: dict) -> Tuple[bool, Optional[str]]:
        """Valida el formato básico del mensaje

        REQ: 1.2, 3.1, 5.1 - Valida el formato básico del mensaje.
        
        Validaciones implementadas:
        1. ✅ Campos requeridos faltantes (REQ: 5.2)
        2. ✅ Tipo de sender válido ('user' o 'system')
        3. ✅ Formato de message_id (REQ: 5.1)
        """
        required_fields = ["message_id", "session_id", "content", "timestamp", "sender"]
        
        for field in required_fields:
            if field not in message_data or not message_data[field]:
                return False, f"Campo requerido faltante: '{field}'"
        
        # Validar sender
        if message_data["sender"] not in ["user", "system"]:
            return False, "El campo 'sender' debe ser 'user' o 'system'"
        
        # Validar formato de message_id
        if not re.match(r'^[a-zA-Z0-9\-_]+$', message_data["message_id"]):
            return False, "message_id solo puede contener letras, números, guiones y guiones bajos"
        
        return True, None
    
    def validate_content(self, content: str) -> Tuple[bool, Optional[str]]:
        """Valida el contenido del mensaje
        
        REQ: 3.2. Valida el contenido del mensaje.
        
        Validaciones implementadas:
        1. Contenido no vacío
        2. Límite de caracteres (1000)
        3. Contenido inapropiado (palabras prohibidas)
                
        """
        if not content or not content.strip():
            return False, "El contenido no puede estar vacío"
        
        if len(content.strip()) > 1000:
            return False, "El contenido no puede exceder 1000 caracteres"
        
        # Validar contenido inapropiado
        # REQUERIMIENTO: 3.2. Validar contenido inapropiado
        content_lower = content.lower()
        for word in self.INAPPROPRIATE_WORDS:
            if word in content_lower:
                return False, f"El contenido contiene palabras inapropiadas"
        
        return True, None
    
def validate_timestamp(self, timestamp_str: str) -> Tuple[bool, Optional[str], Optional[datetime]]:
    """Valida el timestamp y retorna el datetime si es válido"""
    try:
        # REQ: 2.4 - Aceptar múltiples formatos ISO 8601
        # Formato con 'Z' (UTC)
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        
        # Formato sin timezone (asumir UTC)
        elif 'T' in timestamp_str and '+' not in timestamp_str and '-' not in timestamp_str[-6:]:
            timestamp_str = timestamp_str + '+00:00'
        
        # Parsear timestamp
        timestamp = datetime.fromisoformat(timestamp_str)
        
        # Validar que no sea futuro (opcional, pero buena práctica)
        now = datetime.now(timestamp.tzinfo)
        if timestamp > now:
            return False, "El timestamp no puede ser una fecha futura", None
        
        return True, None, timestamp
        
    except (ValueError, AttributeError) as e:
        return False, f"Formato de timestamp inválido. Use ISO 8601 (ej: 2023-06-15T14:30:00Z o 2023-06-15T14:30:00+00:00). Error: {str(e)}", None