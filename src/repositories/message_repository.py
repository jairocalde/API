from src.database.models import Message

class MessageRepository:
    def __init__(self, db):
        self.db = db

    def save_message(self, message_data: dict):
        message = Message(
            message_id=message_data["message_id"],
            session_id=message_data["session_id"],
            content=message_data["content"],
            timestamp=message_data["timestamp"],
            sender=message_data["sender"],
            message_metadata=message_data["metadata"]
        )
        self.db.add(message)
        self.db.commit()
