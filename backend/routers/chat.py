from fastapi import APIRouter, Depends, HTTPException
from models.conversation import Conversation
from schemas.message import Message, MessageSender
from services.chat_service import (
    get_conversation,
    add_message_to_conversation,
    create_conversation
)
from services.ai_service import generate_ai_response
from utils.database import get_db
from bson import ObjectId
from typing import Optional

router = APIRouter()

@router.post("/chat", response_model=Conversation)
async def chat(
    user_message: str,
    user_id: str,
    conversation_id: Optional[str] = None,
    db=Depends(get_db)
):
    """
    Primary chat endpoint that:
    - Accepts user messages
    - Generates AI responses
    - Persists both to database
    """
    
    # Validate user_id
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Get or create conversation
    if conversation_id:
        if not ObjectId.is_valid(conversation_id):
            raise HTTPException(status_code=400, detail="Invalid conversation ID")
        conversation = await get_conversation(db, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = await create_conversation(db, user_id)
        conversation_id = str(conversation.id)
    
    # Create user message
    user_msg = Message(
        text=user_message,
        sender=MessageSender.USER
    )
    
    # Add user message to conversation
    conversation = await add_message_to_conversation(
        db, conversation_id, user_msg
    )
    
    # Generate AI response
    ai_response = await generate_ai_response(
        user_message, 
        conversation.messages
    )
    
    # Create AI message
    ai_msg = Message(
        text=ai_response,
        sender=MessageSender.BOT
    )
    
    # Add AI response to conversation
    conversation = await add_message_to_conversation(
        db, conversation_id, ai_msg
    )
    
    return conversation