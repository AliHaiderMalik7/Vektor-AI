# app/api/routes_model.py
from fastapi import APIRouter, HTTPException
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest
from app.models.response_models import LLMResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
llm_service = LLMService()

@router.post("/generate")
async def generate_llm_response(request: LLMRequest):
    try:
        result = llm_service.generate_chatgpt_response(
            prompt=request.prompt,
            model=request.model,
            system_message=request.system_message,
            enable_web_search=request.enable_web_search,  # ✅ from user input
        )
        return {"response": result}
    except Exception as e:
        return {"detail": str(e)}