from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class MessageSchema(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: Literal["user", "system"]
