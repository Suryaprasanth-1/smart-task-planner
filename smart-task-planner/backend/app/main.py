import os, json
from fastapi import FastAPI, Depends, HTTPException, Header
from dotenv import load_dotenv
from openai import OpenAI

from .models import UserIn, TokenOut, PlanIn, PlanOut
from .auth import hash_pw, verify_pw, create_jwt, decode_jwt

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-70b-versatile")

if LLM_API_KEY:
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
else:
    client = None

app = FastAPI(title="Smart Task Planner API")

# Simple in-memory user store for MVP (swap with Postgres later)
USERS: dict[str, dict] = {}

def require_user(authorization: str = Header(default="")) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = decode_jwt(token, JWT_SECRET)
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/auth/register", response_model=TokenOut)
def register(u: UserIn):
    if not JWT_SECRET:
        raise HTTPException(500, "JWT_SECRET not set")
    if u.email in USERS:
        raise HTTPException(400, "User already exists")
    USERS[u.email] = {"pw": hash_pw(u.password)}
    return {"access_token": create_jwt(u.email, JWT_SECRET)}

@app.post("/auth/login", response_model=TokenOut)
def login(u: UserIn):
    if not JWT_SECRET:
        raise HTTPException(500, "JWT_SECRET not set")
    row = USERS.get(u.email)
    if not row or not verify_pw(u.password, row["pw"]):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_jwt(u.email, JWT_SECRET)}

SYSTEM_PROMPT = """You convert natural language plans into a structured JSON schedule.

Return ONLY valid JSON matching:
{
  "tasks": [
    {"title": "...", "priority": "low|medium|high", "due_date": "YYYY-MM-DD"|null, "duration_minutes": number, "tags": ["..."]}
  ],
  "notes": "..."
}

Rules:
- Keep titles short (<= 10 words).
- Infer sensible durations (15-120 minutes unless clearly longer).
- If no date is specified, set due_date = null.
- Use tags like: work, personal, health, errands, study, finance.
"""

@app.post("/plan", response_model=PlanOut)
def plan(p: PlanIn, user: str = Depends(require_user)):
    if not client:
        raise HTTPException(500, "LLM_API_KEY not set")
    if not LLM_MODEL:
        raise HTTPException(500, "LLM_MODEL not set")

    msg = f"User ({user}) plan:\n{p.text}\nReturn JSON."
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content
    try:
        return json.loads(raw)
    except Exception:
        raise HTTPException(500, f"Model returned non-JSON: {raw}")
