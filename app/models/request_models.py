from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

class LLMRequest(BaseModel):
    
    prompt: str = Field(
        ...,
        description="The prompt to send to the LLM"
        )
    
    model: str = Field(
        default="gpt-4o-mini",
        description="Model to use"
        )
    
    system_message: str = Field(
        default="You are a helpful assistant.",
        description="System message for the LLM"
        )
    
    enable_web_search: bool = Field(
        default = False,
        description = "Enable web search"
    )

    conversation_id: Optional[str] = Field(
        default= None,
        description="Existing conversation ID (for continuing chat)"
    )

    title: Optional[str] = None
    action: Optional[str] = "generate"
    message_id: Optional[str] = None
    content: Optional[str] = None