from sqlalchemy import Column, String, DateTime, JSON
from src.database.database import Base

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    content = Column(String)
    timestamp = Column(DateTime)
    sender = Column(String)
    message_metadata = Column(JSON)
