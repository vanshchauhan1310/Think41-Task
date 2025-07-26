from typing import List
from schemas.message import Message
import random

# Sample product data (would normally come from DB)
SAMPLE_PRODUCTS = [
    {"name": "Premium Cotton T-Shirt", "price": 29.99, "category": "T-Shirts"},
    {"name": "Slim Fit Jeans", "price": 59.99, "category": "Jeans"},
    {"name": "Sports Hoodie", "price": 49.99, "category": "Hoodies"},
]

async def generate_ai_response(user_message: str, conversation_history: List[Message]) -> str:
    """
    Generates appropriate AI responses based on user input.
    In a real implementation, this would connect to an LLM API.
    """
    user_message = user_message.lower()
    
    # Simple intent detection
    if any(word in user_message for word in ["hello", "hi", "hey"]):
        return "Hello! Welcome to our e-commerce store. How can I help you today?"
    
    elif "top product" in user_message or "best seller" in user_message:
        response = "Our top selling products are:\n"
        for i, product in enumerate(SAMPLE_PRODUCTS[:5], 1):
            response += f"{i}. {product['name']} - ${product['price']}\n"
        return response
    
    elif "order status" in user_message:
        return "You can check your order status in the 'My Orders' section of your account."
    
    elif "return" in user_message or "exchange" in user_message:
        return "We accept returns within 30 days of purchase. Please visit our Returns Center for more details."
    
    elif "thank" in user_message:
        return "You're welcome! Is there anything else I can help you with?"
    
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase your question?"