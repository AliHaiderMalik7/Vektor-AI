from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest
from app.database import crud_chat
from app.database.db_session import get_db

router = APIRouter()
llm_service = LLMService()

@router.post("/generate")
async def generate_response_stream(request: LLMRequest, db: Session = Depends(get_db)):

    # Handle conversation creation or fetch
    conv_id = getattr(request, "conversation_id", None)
    if conv_id:
        conversation = crud_chat.get_conversation(db, conv_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = crud_chat.create_conversation(db, title=request.prompt[:50])

    # Optional updates
    if getattr(request, "new_title", None):
        crud_chat.update_conversation_title(db, conversation.id, request.new_title)

    if getattr(request, "update_message_id", None):
        crud_chat.update_message(db, request.update_message_id, request.prompt)

    # Gather conversation history for context
    messages = crud_chat.get_messages_by_conversation(db, conversation.id)
    history = [{"role": m.role, "content": m.content} for m in messages]

    # Store new user message
    user_message = crud_chat.create_message(
        db,
        conversation_id=conversation.id,
        content=request.prompt,
        role="user"
    )

    messages = crud_chat.get_messages_by_conversation(db, conversation.id)
    history_messages = [msg for msg in messages if msg.id != user_message.id]
    history = [{"role": m.role, "content": m.content} for m in history_messages]

    # Stream assistant response with memory
    def response_generator():
        assistant_content = ""
        for chunk in llm_service.generate_chatgpt_response(
            prompt=request.prompt,
            model=request.model,
            stream=True,
            history=history  # ✅ add conversation memory
        ):
            assistant_content += chunk
            yield chunk

        # Save assistant message after streaming
        crud_chat.create_message(
            db,
            conversation_id=conversation.id,
            content=assistant_content,
            role="assistant"
        )

    return StreamingResponse(
        response_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Transfer-Encoding": "chunked",
            "X-Conversation-Id": str(conversation.id),  # 👈 send ID back
        },
    )