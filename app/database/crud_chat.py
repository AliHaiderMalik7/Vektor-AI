from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import models_chat as models
from typing import Optional, List

# Conversation CRUD
def create_conversation(db: Session, title: str = None) -> models.Conversation:
    """Create a new conversation"""
    conv = models.Conversation(title=title or "New Conversation")
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_conversation(db: Session, conversation_id: int) -> Optional[models.Conversation]:
    """Get conversation by ID"""
    return db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()

def get_all_conversations(db: Session, limit: int = 50) -> List[models.Conversation]:
    """Get all conversations ordered by most recent"""
    return db.query(models.Conversation).order_by(
        desc(models.Conversation.updated_at)
    ).limit(limit).all()

def update_conversation_title(db: Session, conversation_id: int, title: str) -> Optional[models.Conversation]:
    """Update conversation title"""
    conv = get_conversation(db, conversation_id)
    if conv:
        conv.title = title
        db.commit()
        db.refresh(conv)
    return conv

def delete_conversation(db: Session, conversation_id: int) -> bool:
    """Delete conversation and all its messages (cascade)"""
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
    """Create a new message in a conversation"""
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
    """Update message content"""
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if msg:
        msg.content = content
        db.commit()
        db.refresh(msg)
    return msg

def delete_message(db: Session, message_id: int) -> bool:
    """Delete a specific message"""
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
    """
    Get all messages for a conversation, ordered chronologically.
    Optionally limit to most recent N messages.
    """
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
    """Get conversation with its messages (useful for response)"""
    conv = get_conversation(db, conversation_id)
    if conv:
        # Preload messages with limit
        conv.messages = get_messages_by_conversation(db, conversation_id, message_limit)
    return conv