# app/database/db_session.py
from prisma import Prisma

# Single shared Prisma client instance
prisma = Prisma()

async def connect_db():
    if not prisma.is_connected():
        await prisma.connect()
        print("✅ Prisma connected.")

async def disconnect_db():
    if prisma.is_connected():
        await prisma.disconnect()
        print("🛑 Prisma disconnected.")
