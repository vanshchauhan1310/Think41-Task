from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class MessageSender(str, Enum):
    USER = "user"
    BOT = "bot"

class Message(BaseModel):
    text: str
    sender: MessageSender
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "text": "What are your top products?",
                "sender": "user",
                "metadata": {"intent": "product_query"}
            }
        }