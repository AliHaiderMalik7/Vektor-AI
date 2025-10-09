import asyncio
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()
    print("✅ Connected to database successfully!")
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
