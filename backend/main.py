from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, conversations
from utils.database import init_db

app = FastAPI(
    title="E-Commerce Chatbot API",
    description="API for managing chatbot conversations",
    version="1.0.0"
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
    await init_db()

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(conversations.router, prefix="/conversations", tags=["conversations"])

@app.get("/")
async def root():
    return {"message": "E-Commerce Chatbot API"}