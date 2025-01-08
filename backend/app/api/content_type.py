from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
#from app.schemas import UserSignup, UserLogin, Token, User

router = APIRouter(prefix="/api/content_type", tags=["content_type"])

@router.get("/")
def get_content_types():
    return {"message": "get content types"}

@router.get("/{content_type_id}/subjects")
def get_content_type(content_type_id: int):
    return {"message": "get content type"}
