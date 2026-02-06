# src/domain/schemas.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
import re

# REQUERIMIENTO: 2. Esquema de Mensaje - Definición de tipos para sender

class SenderType(str, Enum):
    USER = "user"
    SYSTEM = "system"

# REQUERIMIENTO: 2. Esquema de Mensaje - Clase base con todos los campos requeridos

class MessageBase(BaseModel):

    """
    REQUERIMIENTO: 2. Esquema de Mensaje - Define la estructura base de un mensaje.
    
    Campos requeridos implementados:
    1. message_id: Identificador único (string)
    2. session_id: Identificador de sesión (string)
    3. content: Contenido del mensaje (string)
    4. timestamp: Marca de tiempo (formato ISO datetime)
    5. sender: Quién envió el mensaje (string, "user" o "system")
    """
    
    message_id: str = Field(..., min_length=1, max_length=100, description="ID único del mensaje")
    session_id: str = Field(..., min_length=1, max_length=100, description="ID de la sesión")
    content: str = Field(..., min_length=1, max_length=1000, description="Contenido del mensaje")
    timestamp: datetime = Field(..., description="Fecha y hora del mensaje en formato ISO")
    sender: SenderType = Field(..., description="Remitente: 'user' o 'system'")
    
    @validator('message_id')
    def validate_message_id(cls, v):
        if not re.match(r'^[a-zA-Z0-9\-_]+$', v):
            raise ValueError('message_id solo puede contener letras, números, guiones y guiones bajos')
        return v
    
    @validator('timestamp')
    def validate_timestamp(cls, v):
        # Aceptar timestamps con o sin timezone para mayor flexibilidad
        return v
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "message_id": "msg-123456",
                "session_id": "session-abcdef",
                "content": "Hola, ¿cómo estás?",
                "timestamp": "2023-06-15T14:30:00Z",
                "sender": "user"
            }
        }

class MessageCreate(MessageBase):
    """Esquema para creación de mensajes"""
    pass

class Metadata(BaseModel):
    word_count: int = Field(..., description="Número de palabras en el mensaje")
    character_count: int = Field(..., description="Número de caracteres en el mensaje")
    processed_at: datetime = Field(..., description="Fecha y hora de procesamiento")
    is_filtered: bool = Field(False, description="Indica si el contenido fue filtrado")

class MessageWithMetadata(MessageBase):
    metadata: Metadata

class ErrorDetail(BaseModel):
    code: str = Field(..., description="Código de error")
    message: str = Field(..., description="Mensaje de error")
    details: Optional[str] = Field(None, description="Detalles adicionales del error")

class ErrorResponse(BaseModel):
    status: str = Field("error", description="Estado de la respuesta")
    error: ErrorDetail

class SuccessResponse(BaseModel):
    status: str = Field("success", description="Estado de la respuesta")
    data: MessageWithMetadata

class MessageResponse(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    word_count: int
    character_count: int
    processed_at: datetime
    is_filtered: bool
    
    class Config:
        orm_mode = True

class MessageListData(BaseModel):
    session_id: str
    messages: List[MessageResponse]
    pagination: Dict[str, Any]

class MessageListResponse(BaseModel):
    status: str = Field("success", description="Estado de la respuesta")
    data: MessageListData