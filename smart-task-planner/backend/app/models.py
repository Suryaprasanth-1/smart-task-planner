from pydantic import BaseModel, Field
from typing import List, Optional

class UserIn(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PlanIn(BaseModel):
    text: str = Field(..., min_length=3)

class Task(BaseModel):
    title: str
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[str] = None  # YYYY-MM-DD or null
    duration_minutes: int = Field(default=30, ge=5, le=480)
    tags: List[str] = []

class PlanOut(BaseModel):
    tasks: List[Task]
    notes: Optional[str] = None
