from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.conversation import Conversation
from schemas.message import Message
from services.chat_service import (
    create_conversation,
    get_conversation,
    add_message_to_conversation,
    get_user_conversations,
    end_conversation
)
from utils.database import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Conversation)
async def start_conversation(user_id: str, db=Depends(get_db)):
    return await create_conversation(db, user_id)

@router.get("/{conversation_id}", response_model=Conversation)
async def read_conversation(conversation_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(status_code=400, detail="Invalid conversation ID")
    conversation = await get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/{conversation_id}/messages", response_model=Conversation)
async def add_message(
    conversation_id: str, 
    message: Message,
    db=Depends(get_db)
):
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(status_code=400, detail="Invalid conversation ID")
    return await add_message_to_conversation(db, conversation_id, message)

@router.get("/user/{user_id}", response_model=List[Conversation])
async def list_user_conversations(user_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    return await get_user_conversations(db, user_id)

@router.put("/{conversation_id}/end", response_model=Conversation)
async def close_conversation(conversation_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(status_code=400, detail="Invalid conversation ID")
    return await end_conversation(db, conversation_id)