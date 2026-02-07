from datetime import datetime # Importa datetime para validación de fechas

class ValidationService: # Valida que el mensaje tenga todos los campos requeridos

    def validate_message_format(self, message: dict):
        required_fields = ["message_id", "session_id", "content", "timestamp", "sender"]

        for field in required_fields: # Revisa cada campo requerido
            if field not in message:
                return False, f"Falta el campo requerido: {field}" 

        return True, None # Si todos los campos están presentes

    def validate_content(self, content: str):  # Valida que el contenido sea un string no vacío
        if not content or not isinstance(content, str): # Verifica que content no sea None/empty y sea string
            return False, "El contenido del mensaje es inválido"

        return True, None

    def validate_timestamp(self, timestamp): # Valida el formato del timestamp
        if isinstance(timestamp, datetime): # Si ya es un objeto datetime, es válido
            return True, None
        try: # Si es string, intenta parsear como ISO 860
            datetime.fromisoformat(timestamp.replace("Z", "+00:00")) # Reemplaza "Z" (Zulu/UTC) por "+00:00" para compatibilidad
            return True, None
        except Exception:
            return False, "Formato de timestamp inválido. Use ISO 8601 (ej: 2023-06-15T14:30:00Z)"
