from sqlalchemy import Column, String, DateTime, JSON # Importa tipos de columnas SQLAlchemy
from src.database.database import Base # Importa la clase base para modelos

class MessageModel(Base): # Define el modelo de mensaje (mapeo objeto-relacional)
    __tablename__ = "messages"     # Nombre de la tabla en la base de datos

    message_id = Column(String, primary_key=True, index=True)  # message_id: String, clave primaria, con índice para búsquedas rápidas
    session_id = Column(String, index=True) # session_id: String, con índice para búsquedas por sesión
    content = Column(String) # content: String, contenido del mensaje (sin longitud máxima definida)
    timestamp = Column(DateTime) # timestamp: DateTime, fecha/hora del mensaje
    sender = Column(String) # sender: String, remitente del mensaje
    message_metadata = Column(JSON) # message_metadata: JSON, datos adicionales/metadata, JSON permite estructura flexible (diccionario Python)
