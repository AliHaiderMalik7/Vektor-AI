from pydantic import BaseModel, Field, EmailStr, constr
from typing import Optional, Annotated


# LLM Request Schema
class LLMRequest(BaseModel):
    """Request model for generating LLM responses"""

    prompt: str = Field(
        ...,
        description="The prompt or message to send to the LLM"
    )

    model: str = Field(
        default="gpt-4o",
        description="Model to use for generation"
    )

    system_message: str = Field(
        default="You are a helpful fitness assistant.",
        description="System message for the LLM"
    )

    enable_web_search: bool = Field(
        default=False,
        description="Enable web search capability"
    )

    # Fitness-related inputs
    weight_value: Optional[float] = None
    weight_unit: Optional[str] = None
    height_value: Optional[float] = None
    height_unit: Optional[str] = None
    height_extra_inches: Optional[float] = None
    # metadata for chat persistence

    user_id: Optional[int] = Field(
        default=None,
        description="The ID of the user making the request"
    )

    conversation_id: Optional[int] = Field(
        default=None,
        description="Existing conversation ID (if continuing one)"
    )

    new_title: Optional[str] = Field(
        default=None,
        description="Optional new title for the conversation"
    )

    update_message_id: Optional[int] = Field(
        default=None,
        description="If provided, update existing message instead of creating new one"
    )


# Conversation + Message CRUD
class ConversationCreate(BaseModel):
    title: Optional[str]


class ConversationUpdate(BaseModel):
    title: str


class MessageCreate(BaseModel):
    conversation_id: int
    content: str
    role: str


class MessageUpdate(BaseModel):
    content: str


# User Authentication Models

class UserSignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: Annotated[str, constr(min_length=6, max_length=500)]


class UserLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    status: int = 200
    message: str = "Login Successful"
    access_token: str
    refresh_token: str
    token_type: str = "bearer"