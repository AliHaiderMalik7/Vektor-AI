from sqlalchemy.orm import Session
from openai import OpenAI
from app.database.models_chat import Conversation
from app.database.crud_chat import get_messages_by_conversation_id


def generate_and_update_summary(db: Session, conversation_id: int, model="gpt-4o"):
    # Fetch messages
    messages = get_messages_by_conversation_id(db, conversation_id)
    if not messages:
        print(f"No messages found for conversation_id={conversation_id}")
        return None

    # Generate summary
    summary = summarize_messages(messages, model=model)
    if not summary:
        print("❌ Failed to generate summary.")
        return None

    # Update conversation summary
    success = update_conversation_summary(db, conversation_id, summary)
    if not success:
        print("⚠️ Could not update conversation summary in database.")
        return None

    return summary


def summarize_messages(messages, model="gpt-4o"):
    '''
    Summarize the latest user messages (up to 10) using OpenAI API.
    '''
    if not messages:
        return "No messages to summarize."

    # Use only the last 10 messages if more exist
    if len(messages) > 10:
        messages = messages[-10:]

    client = OpenAI()

    # Combine all user message text
    text = "\n".join([m.content for m in messages])
    prompt = (
        f"Summarize the following user conversation messages briefly in 3–5 sentences:\n\n{text}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a concise and helpful summarization assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        print("Error during summarization:", e)
        return None


def update_conversation_summary(db: Session, conversation_id: int, summary: str):
    """
    Update the summary field in the Conversation table for the given conversation_id.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        print(f"Conversation with id={conversation_id} not found.")
        return False

    conversation.summary = summary
    db.commit()
    db.refresh(conversation)
    print(f"Summary updated for conversation_id={conversation_id}")
    return True




