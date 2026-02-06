# src/repositories/message_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc
from src.database.models import MessageModel

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, message, metadata: dict) -> MessageModel:
        db_message = MessageModel(
            message_id=message.message_id,
            session_id=message.session_id,
            content=message.content,
            timestamp=message.timestamp,
            sender=message.sender,
            word_count=metadata.get("word_count", 0),
            character_count=metadata.get("character_count", 0),
            is_filtered=1 if metadata.get("is_filtered", False) else 0
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
    
    def get_by_session_id(
        self, 
        session_id: str, 
        skip: int = 0, 
        limit: int = 100,
        sender: Optional[str] = None
    ) -> List[MessageModel]:
        query = self.db.query(MessageModel).filter(
            MessageModel.session_id == session_id
        )
        
        if sender:
            query = query.filter(MessageModel.sender == sender)
        
        return query.order_by(desc(MessageModel.timestamp)).offset(skip).limit(limit).all()
    
    def get_by_message_id(self, message_id: str) -> Optional[MessageModel]:
        return self.db.query(MessageModel).filter(
            MessageModel.message_id == message_id
        ).first()
    
    def message_exists(self, message_id: str) -> bool:
        return self.get_by_message_id(message_id) is not None
    
    def get_message_count_by_session(self, session_id: str) -> int:
        return self.db.query(MessageModel).filter(
            MessageModel.session_id == session_id
        ).count()