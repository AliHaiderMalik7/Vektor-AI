from prisma import Prisma
from typing import Optional

db = Prisma()

async def connect_db():
    if not db.is_connected():
        await db.connect()

async def create_conversation(user_id: str, title: Optional[str] = None):
    await connect_db()
    return await db.conversation.create(
        data={"userId": user_id, "title": title or "Untitled Conversation"}
    )

async def update_conversation(conversation_id: str, title: str):
    await connect_db()
    return await db.conversation.update(
        where={"id": conversation_id},
        data={"title": title}
    )

async def delete_conversation(conversation_id: str):
    await connect_db()
    return await db.conversation.delete(where={"id": conversation_id})

async def update_message(message_id: str, content: str):
    await connect_db()
    return await db.message.update(
        where={"id": message_id},
        data={"content": content}
    )
