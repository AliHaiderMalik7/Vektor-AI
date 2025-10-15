from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest
from app.database import crud_chat, models_chat
from app.database.db_session import get_db
from app.utils.summarize import generate_and_update_summary
from app.utils.auth import oauth2_scheme, verify_token
from typing import Optional

router = APIRouter()
llm_service = LLMService()


@router.post("/generate")
async def generate_response_stream(
    request: LLMRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    print("\n----------------- 🧠 NEW LLM REQUEST -----------------")

    # --- Step 1: Verify token and user ---
    print("🔐 Verifying user token...")
    username = verify_token(token)
    user = db.query(models_chat.Users).filter(models_chat.Users.username == username).first()
    if not user:
        print("❌ User not found for token")
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id
    print(f"✅ Authenticated user: {user.username} (id={user_id})")

    # --- Step 2: Get conversation_id from frontend ---
    conv_id: Optional[int] = getattr(request, "conversation_id", None)
    if not conv_id:
        print("❌ No conversation_id provided from frontend")
        raise HTTPException(
            status_code=400,
            detail="conversation_id is required from frontend"
        )

    print(f"💬 Checking conversation ownership for ID: {conv_id}")
    conversation = db.query(models_chat.Conversation).filter(
        models_chat.Conversation.id == conv_id
    ).first()

    # --- Step 3: Verify ownership ---
    if not conversation:
        print(f"❌ Conversation not found with id={conv_id}")
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversation.user_id != user_id:
        print(f"🚫 User {user_id} is not the owner of conversation {conv_id}")
        raise HTTPException(status_code=403, detail="Not authorized for this conversation")

    print(f"✅ Conversation {conv_id} verified for user {user_id}")

    # --- Step 4: Save new user message ---
    print(f"💾 Saving new user message to conversation {conv_id}...")
    user_msg = crud_chat.create_message(
        db,
        conversation_id=conv_id,
        content=request.prompt,
        role="user"
    )
    db.commit()
    print(f"✅ User message saved (id={user_msg.id})")

    # --- Step 5: Fetch recent 10 messages for context ---
    print("📚 Fetching last 10 messages for conversation context...")
    messages = (
        db.query(models_chat.Message)
        .filter(models_chat.Message.conversation_id == conv_id)
        .order_by(models_chat.Message.created_at.desc())
        .limit(10)
        .all()
    )
    messages = list(reversed(messages))
    history = [{"role": m.role, "content": m.content} for m in messages]

    print(f"🗂 Found {len(history)} context messages:")
    for m in history:
        print(f"   [{m['role']}] {m['content'][:70]}...")

    # --- Step 6: Add stored summary if available ---
    if conversation.summary:
        print("🧩 Adding stored summary to model context...")
        history.insert(0, {
            "role": "assistant",
            "content": (
                f"Here is a brief summary of the previous conversation:\n\n"
                f"{conversation.summary}\n\n"
                f"Use this summary to maintain continuity."
            )
        })
        print("✅ Summary added to context.")
    else:
        print("⚠️ No summary found for this conversation yet.")

    # --- Step 7: Stream model response ---
    print("🚀 Sending user message + summary + history to LLM...")
    def response_generator():
        assistant_content = ""
        try:
            for chunk in llm_service.generate_chatgpt_response(
                prompt=request.prompt,
                history=history,
                model=request.model,
                stream=True
            ):
                assistant_content += chunk
                yield chunk
        except Exception as e:
            print(f"❌ Error during LLM streaming: {e}")
            yield f"\n[Error: {str(e)}]"

        # --- Save assistant reply ---
        try:
            print("💾 Saving assistant message...")
            crud_chat.create_message(
                db,
                conversation_id=conv_id,
                content=assistant_content,
                role="assistant"
            )
            db.commit()
            print(f"✅ Assistant message saved for conversation {conv_id}")
        except Exception as e:
            print(f"❌ Failed to save assistant message: {e}")

        # --- Update summary after message ---
        print("🧠 Regenerating summary for conversation...")
        try:
            summary = generate_and_update_summary(db, conv_id)
            if summary:
                print(f"✅ Summary updated for conversation {conv_id}")
            else:
                print(f"⚠️ No summary generated for conversation {conv_id}")
        except Exception as e:
            print(f"❌ Error updating summary: {e}")

        print("----------------- ✅ END OF LLM RESPONSE -----------------\n")

    # --- Step 8: Stream response back ---
    return StreamingResponse(
        response_generator(),
        media_type="text/event-stream",
        headers={"X-Conversation-Id": str(conv_id)},
    )
