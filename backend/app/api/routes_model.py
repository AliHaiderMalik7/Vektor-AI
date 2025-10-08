from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest

router = APIRouter()
llm_service = LLMService()

# routes_model.py
@router.post("/generate")
async def generate_response_stream(request: LLMRequest):
    """Simple text streaming"""
    response_generator = llm_service.generate_chatgpt_response(
        prompt=request.prompt,
        model=request.model,
        stream=True
    )
    
    return StreamingResponse(
        response_generator,
        media_type="text/plain"
    )