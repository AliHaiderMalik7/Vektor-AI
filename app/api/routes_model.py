# routes_model.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest
from app.database import crud_chat, models_chat
from app.database.db_session import get_db

router = APIRouter()
llm_service = LLMService()

@router.post("/generate")
async def generate_response_stream(request: LLMRequest, db: Session = Depends(get_db)):

    # Get or fallback to dummy user
    user_id = getattr(request, "user_id", None)
    if not user_id:
        dummy = db.query(models_chat.Users).filter(models_chat.Users.username == "anonymous").first()
        if not dummy:
            dummy = models_chat.Users(
                first_name="Anonymous",
                last_name="User",
                email="anonymous@chat.local",
                username="anonymous",
                password="dummy"
            )
            db.add(dummy)
            db.commit()
            db.refresh(dummy)
        user_id = dummy.id

    # Handle conversation creation or fetch
    conv_id = getattr(request, "conversation_id", None)
    if conv_id:
        conversation = crud_chat.get_conversation(db, conv_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = crud_chat.create_conversation(db, title=request.prompt[:50], user_id=user_id)

    # Update conversation title if provided
    if getattr(request, "new_title", None):
        crud_chat.update_conversation_title(db, conversation.id, request.new_title)

    # Gather history for that conversation (user-specific memory)
    messages = crud_chat.get_messages_by_conversation(db, conversation.id)
    history = [{"role": m.role, "content": m.content} for m in messages]

    # Store user message
    user_message = crud_chat.create_message(
        db,
        conversation_id=conversation.id,
        content=request.prompt,
        role="user"
    )

    # Stream LLM response with per-user memory
    def response_generator():
        assistant_content = ""
        for chunk in llm_service.generate_chatgpt_response(
            prompt=request.prompt,
            history=history,
            model=request.model,
            stream=True
        ):
            assistant_content += chunk
            yield chunk

        crud_chat.create_message(
            db,
            conversation_id=conversation.id,
            content=assistant_content,
            role="assistant"
        )

    return StreamingResponse(
        response_generator(),
        media_type="text/event-stream",
        headers={"X-Conversation-Id": str(conversation.id)},
    )
