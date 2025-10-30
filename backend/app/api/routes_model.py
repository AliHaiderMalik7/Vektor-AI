from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest
from app.database import crud_chat, models_chat
from app.database.db_session import get_db
from app.utils.summarize import generate_and_update_summary
from app.utils.auth import oauth2_scheme, verify_token
from app.utils.attach_media import attach_media_and_enrich
from typing import Optional
import json, re

router = APIRouter()
llm_service = LLMService()


@router.post("/generate")
async def generate_response_stream(
    request: LLMRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    print("NEW LLM REQUEST")

    # Verify token
    username = verify_token(token)
    user = db.query(models_chat.Users).filter(models_chat.Users.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id
    conv_id: Optional[int] = getattr(request, "conversation_id", None)
    if not conv_id:
        raise HTTPException(status_code=400, detail="conversation_id is required")

    conversation = db.query(models_chat.Conversation).filter(
        models_chat.Conversation.id == conv_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    print(f"✅ Conversation {conv_id} verified for user {user_id}")

    # Save user message
    user_msg = crud_chat.create_message(
        db,
        conversation_id=conv_id,
        content=request.prompt,
        role="user"
    )
    db.commit()

    # Get history
    messages = (
        db.query(models_chat.Message)
        .filter(models_chat.Message.conversation_id == conv_id)
        .order_by(models_chat.Message.created_at.desc())
        .limit(10)
        .all()
    )
    messages = list(reversed(messages))
    history = [{"role": m.role, "content": m.content} for m in messages]

    if conversation.summary:
        history.insert(0, {
            "role": "assistant",
            "content": f"Here is a summary of previous conversation:\n{conversation.summary}"
        })

    # Get response from model
    assistant_content = llm_service.generate_chatgpt_response(
        prompt=request.prompt,
        history=history,
        model=request.model,
        weight_value=request.weight_value,
        weight_unit=request.weight_unit,
        height_value=request.height_value,
        height_unit=request.height_unit,
    )

    # Parse response safely
    try:
        if isinstance(assistant_content, dict):
            if "text" in assistant_content and isinstance(assistant_content["text"], str):
                try:
                    parsed_response = json.loads(assistant_content["text"])
                except json.JSONDecodeError:
                    parsed_response = assistant_content
            else:
                parsed_response = assistant_content
        elif isinstance(assistant_content, str):
            parsed_response = json.loads(assistant_content)
        else:
            parsed_response = {"text": str(assistant_content)}
    except Exception as e:
        print(f"❌ Error parsing assistant_content: {e}")
        parsed_response = {"error": f"Failed to parse response: {str(e)}"}

    # Attach exercise media to each exercise in the plan
    parsed_response = attach_media_and_enrich(parsed_response)

    # Save assistant reply
    crud_chat.create_message(
        db,
        conversation_id=conv_id,
        content=json.dumps(parsed_response),
        role="assistant"
    )
    db.commit()

    # Update summary
    try:
        summary = generate_and_update_summary(db, conv_id)
        if summary:
            print(f"✅ Summary updated for conversation {conv_id}")
    except Exception as e:
        print(f"❌ Error updating summary: {e}")

    # Return enriched response
    return {
        "conversation_id": conv_id,
        "response": parsed_response,
    }
