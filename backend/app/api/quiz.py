from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.quiz import QuizResponse, QuizCreate, QuizUpdate, QuizSubmitResponse
from app.models.quiz import Quiz

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])


@router.get("/", response_model=List[QuizResponse])
def get_quizzes(db: Session = Depends(get_db)):
    return db.query(Quiz).all()


@router.post(
    "/",
    response_model=QuizResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            "description": "Quiz already exists",
            "content": {
                "application/json": {"example": {"detail": "Quiz already exists"}}
            },
        }
    },
)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.title == quiz.title).first()
    if db_quiz:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Quiz already exists"
        )

    new_quiz = Quiz(
        title=quiz.title,
        content=quiz.content,
        options=quiz.options,
        subject_id=quiz.subject_id,
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz


@router.get(
    "/{quiz_id}",
    response_model=QuizResponse,
    responses={
        404: {
            "description": "Quiz not found",
            "content": {"application/json": {"example": {"detail": "Quiz not found"}}},
        }
    },
)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )
    return quiz


@router.post(
    "/{quiz_id}/submit",
    response_model=QuizSubmitResponse,
    responses={
        404: {
            "description": "Quiz not found",
            "content": {"application/json": {"example": {"detail": "Quiz not found"}}},
        }
    },
)
def submit_quiz(quiz_id: int, option_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    is_correct = quiz.correct_option_id == option_id
    return QuizSubmitResponse(is_correct=is_correct, detail="Quiz submitted")


@router.put(
    "/{quiz_id}",
    response_model=QuizResponse,
    responses={
        404: {
            "description": "Quiz not found",
            "content": {"application/json": {"example": {"detail": "Quiz not found"}}},
        }
    },
)
def update_quiz(quiz_id: int, quiz: QuizUpdate, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )
    db_quiz.title = quiz.title
    db_quiz.content = quiz.content
    db_quiz.options = quiz.options
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


@router.delete(
    "/{quiz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "description": "Quiz not found",
            "content": {"application/json": {"example": {"detail": "Quiz not found"}}},
        }
    },
)
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )
    db.delete(db_quiz)
    db.commit()
    return {"detail": "Quiz deleted"}
