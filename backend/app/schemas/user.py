from pydantic import BaseModel, EmailStr
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
    # TODO: User DB Model에 updated_at이 업데이트되는 시점 파악 후 수정
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
