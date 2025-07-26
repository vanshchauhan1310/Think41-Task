import os
import json
from groq import Groq
from typing import List, Dict
from models.conversation import Conversation
from schemas.message import Message
from utils.database import get_db
import logging
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.db = MongoClient(os.getenv("MONGO_URI"))[os.getenv("DB_NAME")]
        
    async def generate_response(self, user_message: str, conversation_history: List[Message]) -> str:
        """
        Generates an AI response using Groq's LLM with business logic integration
        """
        try:
            # Format conversation history
            messages = self._format_conversation_history(conversation_history)
            
            # Get system prompt with business logic instructions
            system_prompt = self._get_system_prompt()
            
            # Call Groq API
            response = self.client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}] + messages,
                model="mixtral-8x7b-32768",  # or "llama2-70b-4096"
                temperature=0.3,
                max_tokens=1024
            )
            
            # Extract and process response
            llm_response = response.choices[0].message.content
            
            # Check if we need to query the database
            if "<<QUERY_DB>>" in llm_response:
                return await self._handle_db_query(llm_response, user_message)
                
            return llm_response
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return "I'm having trouble processing your request. Please try again later."

    def _format_conversation_history(self, history: List[Message]) -> List[Dict]:
        """Formats message history for LLM input"""
        return [
            {
                "role": "user" if msg.sender == "user" else "assistant",
                "content": msg.text
            }
            for msg in history
        ]
    
    def _get_system_prompt(self) -> str:
        """System prompt with business logic instructions"""
        return """
        You are an AI assistant for an e-commerce clothing store. Your role is to:
        1. Ask clarifying questions when needed to understand customer requests
        2. Query the database when appropriate (use <<QUERY_DB>> marker)
        3. Provide helpful, accurate information about products
        
        Guidelines:
        - Be polite and professional
        - Keep responses concise but informative
        - For product inquiries, always verify availability
        - For order status requests, ask for order number
        
        Database Query Instructions:
        When you need to query the database, respond with:
        <<QUERY_DB>>[your natural language query]
        
        Example:
        User: "What are your top jeans?"
        AI: "<<QUERY_DB>>Get top 5 jeans sorted by sales count"
        """

    async def _handle_db_query(self, llm_response: str, user_message: str) -> str:
        """Handles database queries triggered by the LLM"""
        try:
            query = llm_response.split("<<QUERY_DB>>")[1].strip()
            logger.info(f"Executing database query: {query}")
            
            # Parse query and execute appropriate database operation
            if "top" in query.lower() and "product" in query.lower():
                products = await self._query_top_products(query)
                return self._format_product_response(products)
            elif "order status" in query.lower():
                return "Please provide your order number so I can check the status."
            else:
                return "I need more information to help with that request. Could you please clarify?"
                
        except Exception as e:
            logger.error(f"Error handling DB query: {e}")
            return "I encountered an error processing your request. Please try again."

    async def _query_top_products(self, query: str) -> List[Dict]:
        """Queries top products based on LLM request"""
        try:
            limit = 5
            if "3" in query:
                limit = 3
            elif "5" in query:
                limit = 5
            elif "10" in query:
                limit = 10
                
            category = None
            if "jeans" in query.lower():
                category = "Jeans"
            elif "shirt" in query.lower():
                category = "T-Shirts"
                
            query_filter = {}
            if category:
                query_filter["category"] = category
                
            products = await self.db.products.find(query_filter)\
                .sort("salesCount", -1)\
                .limit(limit)\
                .to_list(length=limit)
                
            return products
            
        except Exception as e:
            logger.error(f"Error querying products: {e}")
            raise

    def _format_product_response(self, products: List[Dict]) -> str:
        """Formats product data for LLM response"""
        if not products:
            return "We don't have any products matching that criteria currently."
            
        response = "Here are our top products:\n"
        for i, product in enumerate(products, 1):
            response += (
                f"{i}. {product['name']} - ${product['price']} "
                f"(Category: {product['category']})\n"
            )
        response += "\nWould you like more information about any of these?"
        return response