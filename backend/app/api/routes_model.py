# from fastapi import APIRouter
# from app.services.llm_service import LLMService
# from app.models.request_models import ChatRequest
# from app.models.response_models import ChatResponse

# router = APIRouter()
# llm_service = LLMService()

# @router.post("/chat", response_model=ChatResponse)
# async def chat_with_model(request: ChatRequest):
#     reply = llm_service.generate_response(request.prompt)
#     return ChatResponse(response=reply)
