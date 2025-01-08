from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
#from app.schemas import Quiz, AnswerSubmit, AnswerWithFeedback
from typing import List, Optional
from app.services import quiz_service

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])

@router.get("/")
def get_quizzes():
    return {"message": "get quizzes"}

@router.get("/{quiz_id}")
def get_quiz(quiz_id: int):
    return {"message": "get quiz"}

@router.post("/{quiz_id}/submit")
def submit_answer(quiz_id: int):
    return {"message": "submit answer"}