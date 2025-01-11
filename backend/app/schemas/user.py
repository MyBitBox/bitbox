from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    nickname: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ContentTypeProgress(BaseModel):
    id: int
    name: str
    description: str


class SubjectProgress(BaseModel):
    id: int
    name: str
    description: str
    content_type_id: int
    progress_rate: float


class UserProgressResponse(BaseModel):
    total_quizzes: int
    correct_rate: float
    content_types: List[ContentTypeProgress]
    subjects: List[SubjectProgress]
    last_update: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
