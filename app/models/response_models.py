from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LLMResponse(BaseModel):
    response: str

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    content: str
    role: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ConversationResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    messages: List[MessageResponse] = []

    class Config:
        orm_mode = True