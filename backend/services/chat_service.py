from datetime import datetime
from bson import ObjectId
from models.conversation import Conversation
from schemas.message import Message
from typing import List

async def create_conversation(db, user_id: str):
    session_id = f"session_{datetime.utcnow().timestamp()}"
    conversation = {
        "user_id": ObjectId(user_id),
        "session_id": session_id,
        "messages": [],
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = await db.conversations.insert_one(conversation)
    return await get_conversation(db, str(result.inserted_id))

async def get_conversation(db, conversation_id: str):
    conversation = await db.conversations.find_one({"_id": ObjectId(conversation_id)})
    if conversation:
        return Conversation(**conversation)
    return None

async def add_message_to_conversation(db, conversation_id: str, message: Message):
    message_dict = message.dict()
    message_dict["timestamp"] = datetime.utcnow()
    
    await db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$push": {"messages": message_dict},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    return await get_conversation(db, conversation_id)

async def get_user_conversations(db, user_id: str):
    conversations = []
    async for conversation in db.conversations.find({"user_id": ObjectId(user_id)}).sort("updated_at", -1):
        conversations.append(Conversation(**conversation))
    return conversations

async def end_conversation(db, conversation_id: str):
    await db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    return await get_conversation(db, conversation_id)