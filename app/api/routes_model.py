# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse
# from app.services.llm_service import LLMService
# from app.models.request_models import LLMRequest

# router = APIRouter()
# llm_service = LLMService()

# # routes_model.py
# @router.post("/generate")
# async def generate_response_stream(request: LLMRequest):
#     """Simple text streaming"""
#     response_generator = llm_service.generate_chatgpt_response(
#         prompt=request.prompt,
#         model=request.model,
#         stream=True
#     )
#     return StreamingResponse(
#     response_generator,
#     media_type="text/event-stream",  # 👈 SSE mode
#     headers={
#         "Cache-Control": "no-cache",
#         "Connection": "keep-alive",
#         "Transfer-Encoding": "chunked"
#     }
# )



from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest
from app.database import crud_chat

router = APIRouter()
llm_service = LLMService()

@router.post("/generate")
async def generate_response_stream(request: LLMRequest):
    """
    Extended API: 
    - Manage conversation/message CRUD
    - Stream LLM responses
    """

    action = request.action or "generate"

    # --- Conversation + Message CRUD Actions ---
    if action == "create_conversation":
        convo = await crud_chat.create_conversation(user_id="default-user", title=request.title)
        return JSONResponse({"status": "success", "conversation": convo.dict()})

    elif action == "update_conversation":
        if not request.conversation_id or not request.title:
            raise HTTPException(status_code=400, detail="conversation_id and title are required")
        convo = await crud_chat.update_conversation(request.conversation_id, request.title)
        return JSONResponse({"status": "success", "conversation": convo.dict()})

    elif action == "delete_conversation":
        if not request.conversation_id:
            raise HTTPException(status_code=400, detail="conversation_id is required")
        convo = await crud_chat.delete_conversation(request.conversation_id)
        return JSONResponse({"status": "deleted", "conversation": convo.dict()})

    elif action == "update_message":
        if not request.message_id or not request.content:
            raise HTTPException(status_code=400, detail="message_id and content are required")
        msg = await crud_chat.update_message(request.message_id, request.content)
        return JSONResponse({"status": "success", "message": msg.dict()})

    # --- Default: Generate LLM Response (streaming) ---
    elif action == "generate":
        response_generator = llm_service.generate_chatgpt_response(
            prompt=request.prompt,
            model=request.model,
            stream=True
        )
        return StreamingResponse(
            response_generator,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Transfer-Encoding": "chunked"
            }
        )

    else:
        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")
