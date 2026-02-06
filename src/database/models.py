# src/database/models.py
from sqlalchemy import Column, String, DateTime, Integer, Text, Index
from sqlalchemy.sql import func
from .database import Base

# REQ: 1.3 y 2 - Modelo de Base de Datos para almacenamiento de mensajes

class MessageModel(Base):

    """
    REQ: 1.3. Modelo para almacenar mensajes en la base de datos.
    REQ: 2. Estructura que refleja el esquema de mensaje requerido.
    
    Campos correspondientes a REQ: 2:
    1. message_id: Identificador único (string) - único e indexado
    2. session_id: Identificador de sesión (string) - indexado
    3. content: Contenido del mensaje (string) - Text para contenido largo
    4. timestamp: Marca de tiempo (DateTime) - almacenado como datetime
    5. sender: Remitente (string) - 'user' o 'system'
    
    Campos adicionales para procesamiento (REQ: 3.3):
    6. word_count: Conteo de palabras
    7. character_count: Conteo de caracteres
    8. processed_at: Fecha de procesamiento
    9. is_filtered: Indicador de contenido filtrado
    
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True, nullable=False) #Identificador único, índice único
    session_id = Column(String, index=True, nullable=False) #Identificador de sesión, indexado para búsquedas rápidas
    content = Column(Text, nullable=False) #contenido del mensaje (Text permite contenido largo)
    timestamp = Column(DateTime, nullable=False) #Marca de tiempo almacenada como DateTime
    sender = Column(String, nullable=False) # Remitente ('user' o 'system')
    word_count = Column(Integer, default=0) #Metadato: conteo de palabras
    character_count = Column(Integer, default=0) #Metadato: conteo de caracteres
    processed_at = Column(DateTime, server_default=func.now())   # Campo para fecha de procesamiento
    is_filtered = Column(Integer, default=0)  # 0 = no filtrado, 1 = filtrado
    
    # Índices compuestos para mejor performance
    __table_args__ = (
        # REQ: 4. Índice para búsquedas por sesión y timestamp (paginación ordenada)
        Index('ix_session_timestamp', 'session_id', 'timestamp'),

        # REQ: 4.3. Índice para filtrado por remitente y sesión
        Index('ix_sender_session', 'sender', 'session_id'),
    )
    
    def __repr__(self):
        return f"<Message(id={self.id}, message_id='{self.message_id}', session='{self.session_id}')>"