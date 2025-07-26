# Think41 Task: Full-Stack Chatbot Application

## Overview
This project is a full-stack chatbot application with a React (Vite) frontend, FastAPI backend, and MongoDB database. It supports real-time chat, conversation history, and is fully containerized for easy deployment.

## Features
- Chat with AI (LLM integration)
- Conversation history panel
- User and order management
- Full Docker support (backend, frontend, MongoDB)

## Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)

## Quick Start (Recommended)

1. **Clone the repository:**
   ```sh
   git clone https://github.com/vanshchauhan1310/Think41-Task.git
   cd Think41-Task
   ```

2. **Start all services:**
   ```sh
   docker-compose up --build
   ```
   - This will build and start the backend (FastAPI), frontend (React), and MongoDB database.

3. **Access the app:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
   - MongoDB: `localhost:27017`

## Project Structure
```
Think41-Task/
  backend/         # FastAPI backend
  src/             # React frontend (Vite)
  docker-compose.yml
  Dockerfile       # Frontend Dockerfile
  README.md
```

## Environment Variables
- The backend expects `MONGO_URL` (set automatically in docker-compose).
- For local development, create a `.env` file in `backend/`:
  ```env
  MONGO_URL=mongodb://localhost:27017
  ```

## Useful Commands
- **Build and start all services:**
  ```sh
  docker-compose up --build
  ```
- **Stop all services:**
  ```sh
  docker-compose down
  ```
- **Rebuild a single service:**
  ```sh
  docker-compose build backend
  docker-compose build frontend
  ```

## Development (without Docker)
- **Backend:**
  ```sh
  cd backend
  pip install -r requirements.txt
  uvicorn main:app --reload
  ```
- **Frontend:**
  ```sh
  npm install
  npm run dev
  ```

## Troubleshooting
- Ensure Docker Desktop is running.
- If ports are in use, stop other services or change the ports in `docker-compose.yml`.
- For MongoDB connection issues, check the `MONGO_URL` and that the `mongo` service is healthy.

## License
MIT
