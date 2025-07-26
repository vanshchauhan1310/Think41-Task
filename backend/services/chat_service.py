from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from models.conversation import Conversation
from schemas.message import Message
from pymongo.errors import PyMongoError
import logging

logger = logging.getLogger(__name__)

async def create_conversation(db, user_id: str) -> Conversation:
    """
    Creates a new conversation for a user
    Args:
        db: MongoDB database connection
        user_id: ID of the user starting the conversation
    Returns:
        Conversation object
    """
    try:
        session_id = f"session_{datetime.utcnow().timestamp()}"
        conversation_data = {
            "user_id": ObjectId(user_id),
            "session_id": session_id,
            "messages": [],
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.conversations.insert_one(conversation_data)
        if not result.inserted_id:
            raise ValueError("Failed to create conversation")
        
        # Return the full conversation object
        return await get_conversation(db, str(result.inserted_id))
    
    except PyMongoError as e:
        logger.error(f"Database error creating conversation: {e}")
        raise
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise

async def get_conversation(db, conversation_id: str) -> Optional[Conversation]:
    """
    Retrieves a conversation by ID
    Args:
        db: MongoDB database connection
        conversation_id: ID of the conversation to retrieve
    Returns:
        Conversation object or None if not found
    """
    try:
        conversation = await db.conversations.find_one({"_id": ObjectId(conversation_id)})
        if conversation:
            return Conversation(**conversation)
        return None
    except PyMongoError as e:
        logger.error(f"Database error getting conversation: {e}")
        raise

async def add_message_to_conversation(
    db, 
    conversation_id: str, 
    message: Message
) -> Conversation:
    """
    Adds a message to an existing conversation
    Args:
        db: MongoDB database connection
        conversation_id: ID of the conversation
        message: Message object to add
    Returns:
        Updated Conversation object
    """
    try:
        message_dict = message.dict()
        message_dict["timestamp"] = datetime.utcnow()
        
        update_result = await db.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$push": {"messages": message_dict},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if update_result.modified_count == 0:
            raise ValueError("Failed to add message to conversation")
        
        return await get_conversation(db, conversation_id)
    except PyMongoError as e:
        logger.error(f"Database error adding message: {e}")
        raise
    except Exception as e:
        logger.error(f"Error adding message: {e}")
        raise

async def get_user_conversations(db, user_id: str) -> List[Conversation]:
    """
    Gets all conversations for a specific user
    Args:
        db: MongoDB database connection
        user_id: ID of the user
    Returns:
        List of Conversation objects
    """
    try:
        conversations = []
        async for conversation in db.conversations.find(
            {"user_id": ObjectId(user_id)}
        ).sort("updated_at", -1):
            conversations.append(Conversation(**conversation))
        return conversations
    except PyMongoError as e:
        logger.error(f"Database error getting user conversations: {e}")
        raise

async def end_conversation(db, conversation_id: str) -> Conversation:
    """
    Marks a conversation as inactive
    Args:
        db: MongoDB database connection
        conversation_id: ID of the conversation to end
    Returns:
        Updated Conversation object
    """
    try:
        update_result = await db.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$set": {
                    "is_active": False,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if update_result.modified_count == 0:
            raise ValueError("Failed to end conversation")
        
        return await get_conversation(db, conversation_id)
    except PyMongoError as e:
        logger.error(f"Database error ending conversation: {e}")
        raise
    except Exception as e:
        logger.error(f"Error ending conversation: {e}")
        raise

async def get_conversation_messages(db, conversation_id: str) -> List[Message]:
    """
    Gets all messages from a specific conversation
    Args:
        db: MongoDB database connection
        conversation_id: ID of the conversation
    Returns:
        List of Message objects
    """
    try:
        conversation = await db.conversations.find_one(
            {"_id": ObjectId(conversation_id)},
            {"messages": 1}
        )
        if conversation:
            return [Message(**msg) for msg in conversation.get("messages", [])]
        return []
    except PyMongoError as e:
        logger.error(f"Database error getting messages: {e}")
        raise