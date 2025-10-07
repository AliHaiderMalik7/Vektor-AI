from pydantic import BaseModel, Field

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