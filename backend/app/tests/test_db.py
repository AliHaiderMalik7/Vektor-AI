from app.database.db_session import Base, engine
from app.database.models_chat import Users, Conversation, Message

print("Creating all tables in the database...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
