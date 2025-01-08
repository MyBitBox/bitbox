from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup")
def signup():
    return {"message": "signup"}

@router.post("/login")
def login():
    return {"message": "login"}

@router.post("/logout")
def logout():
    return {"message": "logout"}