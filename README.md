# Smart Task Planner – AI Productivity Agent

AI-powered agent that converts natural language plans into structured task schedules.

## Features
- Natural language → JSON task planning
- Priority, deadlines, duration inference
- JWT authentication
- Dockerized backend
- React + TypeScript frontend

## Tech Stack
FastAPI, React, TypeScript, LLM API (Groq/OpenAI), JWT, Docker

## Run Locally
### Backend
cd backend  
cp .env.example .env  
pip install -r requirements.txt  
uvicorn main:app --reload  

### Frontend
cd frontend  
npm install  
npm run dev
