from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "ecommerce_chatbot")

client = None
db = None

async def init_db():
    global client, db
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]
        # Create indexes
        await db.conversations.create_index("user_id")
        await db.conversations.create_index("session_id", unique=True)
        await db.conversations.create_index("is_active")
        await db.conversations.create_index("updated_at")
        print("✅ Database connection established and indexes created")
    except ConnectionFailure as e:
        print(f"❌ Could not connect to MongoDB: {e}")
        raise

def get_db():
    return db