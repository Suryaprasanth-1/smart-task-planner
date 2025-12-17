# Smart Task Planner – AI Productivity Agent

A small full‑stack app that converts natural language plans into structured tasks (JSON) using an OpenAI‑compatible LLM API.

## Features
- Natural language → task schedule (priority, duration, tags, optional due dates)
- JWT auth (register/login)
- FastAPI backend
- React + TypeScript frontend (Vite)
- Dockerized backend

## Tech Stack
FastAPI, Python, React, TypeScript, JWT, Docker, OpenAI SDK (works with Groq/OpenAI-compatible endpoints)

## Run locally (recommended)
### Backend
```bash
cd backend
cp .env.example .env
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

## Environment
Backend uses:
- `JWT_SECRET` (required)
- `LLM_API_KEY` (required)
- `LLM_BASE_URL` (default Groq OpenAI-compatible)
- `LLM_MODEL` (default llama-3.1-70b-versatile)

## Docker (backend only)
```bash
cd backend
docker build -t smart-task-planner-backend .
docker run --rm -p 8000:8000 --env-file .env smart-task-planner-backend
```
