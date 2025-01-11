from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserUpdate, UserProgressResponse
from app.core.utils import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.answer import Answer
from app.models.subject import Subject
from app.models.content_type import ContentType
from app.models.quiz import Quiz
from app.schemas.user import SubjectProgress, ContentTypeProgress


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    responses={
        404: {
            "description": "User not found",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        }
    },
)
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.user.nickname = user_update.nickname
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/me/progress", response_model=UserProgressResponse)
async def get_user_progress(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # 사용자의 모든 답변 가져오기
    answers = db.query(Answer).filter(Answer.user_id == current_user.id).all()

    # 총 퀴즈 수와 정답률 계산
    total_quizzes = len(answers)
    correct_answers = len([a for a in answers if a.is_correct])
    correct_rate = correct_answers / total_quizzes if total_quizzes > 0 else 0

    # 사용자가 참여한 모든 과목 ID 수집
    subject_ids = {answer.subject_id for answer in answers}

    # 참여한 과목들의 정보 가져오기
    subjects = db.query(Subject).filter(Subject.id.in_(subject_ids)).all()

    # 참여한 콘텐츠 타입 ID 수집
    content_type_ids = {subject.content_type_id for subject in subjects}

    # 참여한 콘텐츠 타입 정보 가져오기
    content_types = (
        db.query(ContentType).filter(ContentType.id.in_(content_type_ids)).all()
    )

    # 과목별 진행률 계산
    subject_progress = []
    for subject in subjects:
        subject_answers = [a for a in answers if a.subject_id == subject.id]
        subject_quizzes = db.query(Quiz).filter(Quiz.subject_id == subject.id).count()
        progress_rate = (
            len(subject_answers) / subject_quizzes if subject_quizzes > 0 else 0
        )

        subject_progress.append(
            SubjectProgress(
                id=subject.id,
                name=subject.name,
                description=subject.description,
                content_type_id=subject.content_type_id,
                progress_rate=progress_rate,
            )
        )

    # 콘텐츠 타입 정보 변환
    content_type_progress = [
        ContentTypeProgress(id=ct.id, name=ct.name, description=ct.description)
        for ct in content_types
    ]

    return UserProgressResponse(
        total_quizzes=total_quizzes,
        correct_rate=correct_rate,
        content_types=content_type_progress,
        subjects=subject_progress,
        last_update=datetime.now(),
    )
