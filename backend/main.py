from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, conversations, chat
from utils.database import init_db
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="E-Commerce Chatbot API",
    description="API for managing chatbot conversations and messages",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection
@app.on_event("startup")
async def startup_db_client():
    try:
        await init_db()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Chatbot API is running"}

@app.get("/")
async def root():
    return {
        "message": "E-Commerce Chatbot API",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }