from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

# from app.schemas import UserSignup, UserLogin, Token, User

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
def get_me():
    return {"message": "get me"}


@router.put("/me")
def update_me():
    return {"message": "update me"}
