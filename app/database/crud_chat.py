from sqlalchemy.orm import Session
from app.database import models_chat as models

# Conversation CRUD
def create_conversation(db: Session, title: str = None):
    conv = models.Conversation(title=title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_conversation(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def update_conversation_title(db: Session, conversation_id: int, title: str):
    conv = get_conversation(db, conversation_id)
    if conv:
        conv.title = title
        db.commit()
        db.refresh(conv)
    return conv

def delete_conversation(db: Session, conversation_id: int):
    conv = get_conversation(db, conversation_id)
    if conv:
        db.delete(conv)
        db.commit()
    return conv

# Message CRUD
def create_message(db: Session, conversation_id: int, content: str, role: str):
    msg = models.Message(conversation_id=conversation_id, content=content, role=role)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def update_message(db: Session, message_id: int, content: str):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if msg:
        msg.content = content
        db.commit()
        db.refresh(msg)
    return msg

def get_messages_by_conversation(db: Session, conversation_id: int):
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()
