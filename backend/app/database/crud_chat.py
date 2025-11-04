from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import models_chat as models
from typing import Optional, List

# Conversation CRUD

# crud_chat.py
def create_conversation(db: Session, title: str = None, user_id: int = None, summary: str = "") -> models.Conversation:
    """Create a new conversation"""
    conv = models.Conversation(
        title=title or "New Conversation",
        user_id=user_id,
        summary=summary
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def get_user_conversations(db: Session, user_id: int):
    return db.query(models.Conversation).filter(models.Conversation.user_id == user_id).order_by(
        desc(models.Conversation.updated_at)
    ).all()

def get_conversation(db: Session, conversation_id: int) -> Optional[models.Conversation]:
    return db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()

def get_all_conversations(db: Session, limit: int = 50) -> List[models.Conversation]:
    return db.query(models.Conversation).order_by(
        desc(models.Conversation.updated_at)
    ).limit(limit).all()

def update_conversation_title(db: Session, conversation_id: int, title: str) -> Optional[models.Conversation]:
    conv = get_conversation(db, conversation_id)
    if conv:
        conv.title = title
        db.commit()
        db.refresh(conv)
    return conv

def delete_conversation(db: Session, conversation_id: int) -> bool:
    conv = get_conversation(db, conversation_id)
    if conv:
        db.delete(conv)
        db.commit()
        return True
    return False

# Message CRUD
def create_message(
    db: Session, 
    conversation_id: int, 
    content: str, 
    role: str
) -> models.Message:
    msg = models.Message(
        conversation_id=conversation_id, 
        content=content, 
        role=role
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def update_message(db: Session, message_id: int, content: str) -> Optional[models.Message]:
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if msg:
        msg.content = content
        db.commit()
        db.refresh(msg)
    return msg

def delete_message(db: Session, message_id: int) -> bool:
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if msg:
        db.delete(msg)
        db.commit()
        return True
    return False

def get_messages_by_conversation(
    db: Session, 
    conversation_id: int,
    limit: Optional[int] = None
) -> List[models.Message]:

    query = db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).order_by(models.Message.created_at)
    
    if limit:
        # Get total count
        total = query.count()
        # Skip older messages if over limit
        if total > limit:
            query = query.offset(total - limit)
    
    return query.all()

def get_conversation_with_messages(
    db: Session, 
    conversation_id: int,
    message_limit: Optional[int] = None
) -> Optional[models.Conversation]:
    conv = get_conversation(db, conversation_id)
    if conv:
        # Preload messages with limit
        conv.messages = get_messages_by_conversation(db, conversation_id, message_limit)
    return conv

def get_messages_by_conversation_id(db: Session, conversation_id: int):
    messages = (
        db.query(models.Message)
        .filter(
            models.Message.conversation_id == conversation_id,
            models.Message.role == "user"
        )
        .order_by(models.Message.created_at.asc())
        .all()
    )
    return messages

def get_conversations_by_user_id(db: Session, user_id: int):
    conversations = (
        db.query(models.Conversation)
        .filter(models.Conversation.user_id == user_id)
        .order_by(models.Conversation.updated_at.desc())
        .all()
    )
    return conversations

# Image CRUD
# Image CRUD
def create_image_record(
    db: Session, 
    user_id: int, 
    file_path: str, 
    file_name: str, 
    conversation_id: int = None, 
    file_type: str = "image/jpeg"
):
    from app.database import models_chat as models
    img = models.Image(
        user_id=user_id,
        conversation_id=conversation_id,
        file_path=file_path,
        file_name=file_name,
        file_type=file_type
    )
    db.add(img)
    db.commit()
    db.refresh(img)
    return img


def get_images_by_user(db: Session, user_id: int):
    from app.database import models_chat as models
    return db.query(models.Image).filter(models.Image.user_id == user_id).all()


def get_image_by_id(db: Session, image_id: int):
    from app.database import models_chat as models
    return db.query(models.Image).filter(models.Image.id == image_id).first()
