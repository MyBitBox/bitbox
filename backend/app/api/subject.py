from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
# from app.schemas import UserSignup, UserLogin, Token, User
from app.services import auth_service

router = APIRouter(prefix="/api/subjects", tags=["subjects"])

@router.get("/")
def get_subjects():
    return {"message": "get subjects"}