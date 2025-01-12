from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.openai import generate_quiz_feedback
from app.core.utils import get_current_user
from app.schemas.quiz import QuizResponse, QuizCreate, QuizUpdate, QuizSubmitResponse
from app.models.quiz import Quiz, QuizType
from app.models.answer import Answer
from app.models.user import User

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])


@router.get("/", response_model=List[QuizResponse])
def get_quizzes(subject_id: int, db: Session = Depends(get_db)):
    return db.query(Quiz).filter(Quiz.subject_id == subject_id).all()


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
    # 타입별 필드 유효성 검사
    quiz.validate_fields()

    db_quiz = db.query(Quiz).filter(Quiz.title == quiz.title).first()
    if db_quiz:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Quiz already exists"
        )

    new_quiz = Quiz(
        title=quiz.title,
        content=quiz.content,
        type=quiz.type,
        subject_id=quiz.subject_id,
        options=(
            [option.model_dump() for option in quiz.options] if quiz.options else None
        ),
        correct_option_id=quiz.correct_option_id,
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
        404: {"description": "Quiz not found"},
        400: {"description": "Invalid quiz submission"},
        500: {"description": "Internal server error"},
    },
)
async def submit_quiz(
    quiz_id: int,
    option_id: Optional[int] = Body(None),
    content: Optional[str] = Body(None),
    time_taken: Optional[int] = Body(default=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(
        f"[DEBUG] Received quiz submission - quiz_id: {quiz_id}, option_id: {option_id}, content: {content}"
    )

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        print(f"[DEBUG] Quiz not found - quiz_id: {quiz_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    print(f"[DEBUG] Quiz type: {quiz.type}")

    # 퀴즈 타입에 따른 처리
    if quiz.type == QuizType.MULTIPLE_CHOICE:
        if option_id is None:
            print(f"[DEBUG] Missing option_id for multiple choice quiz")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Multiple choice quiz requires option_id",
            )
        is_correct = quiz.correct_option_id == option_id
        try:
            selected_option = next(
                opt for opt in quiz.options if opt["id"] == option_id
            )
            correct_option = next(
                opt for opt in quiz.options if opt["id"] == quiz.correct_option_id
            )
        except StopIteration:
            print(f"[DEBUG] Invalid option_id: {option_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid option_id",
            )
        selected_content = selected_option["content"]
        correct_content = None if is_correct else correct_option["content"]
    else:
        if content is None:
            print(f"[DEBUG] Missing content for {quiz.type.value} quiz")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{quiz.type.value} quiz requires content",
            )
        selected_content = content
        correct_content = None
        is_correct = None  # OpenAI 피드백에서 결정됨

    try:
        print(
            f"[DEBUG] Generating feedback - quiz_type: {quiz.type.value}, selected_content: {selected_content[:100]}..."
        )
        # OpenAI를 통한 피드백 생성
        feedback = await generate_quiz_feedback(
            quiz_title=quiz.title,
            quiz_content=quiz.content,
            selected_content=selected_content,
            correct_content=correct_content,
            is_correct=is_correct,
            quiz_type=quiz.type.value,
        )
        print(f"[DEBUG] Feedback generated successfully")

        # 코딩 테스트와 텍스트 답변의 경우 OpenAI 피드백에서 정답 여부 추출
        if quiz.type != QuizType.MULTIPLE_CHOICE:
            # 피드백 첫 부분에서 정답 여부 확인
            is_correct = any(
                marker in feedback.lower()[:50]
                for marker in [
                    "정답입니다",
                    "훌륭합니다",
                    "좋은 답변입니다",
                    "테스트 통과",
                    "잘 작성하셨습니다",
                ]
            )

        # 기존 시도 횟수 확인 및 업데이트
        existing_answer = (
            db.query(Answer)
            .filter(Answer.quiz_id == quiz_id, Answer.user_id == current_user.id)
            .first()
        )
        if existing_answer:
            print(
                f"[DEBUG] Updating existing answer - retry_count: {existing_answer.retry_count + 1}"
            )
            existing_answer.retry_count += 1
            existing_answer.is_correct = is_correct
            existing_answer.content = selected_content
            existing_answer.option_id = option_id
            existing_answer.time_taken = time_taken
            existing_answer.feedback_content = feedback
            db.add(existing_answer)
        else:
            print(f"[DEBUG] Creating new answer")
            new_answer = Answer(
                quiz_id=quiz_id,
                user_id=current_user.id,
                option_id=option_id,
                content=selected_content,
                is_correct=is_correct,
                feedback_content=feedback,
                subject_id=quiz.subject_id,
                retry_count=1,
                time_taken=time_taken,
            )
            db.add(new_answer)

        db.commit()
        print(f"[DEBUG] Answer saved successfully")

        return QuizSubmitResponse(is_correct=is_correct, detail=feedback)
    except Exception as e:
        print(f"[ERROR] Error in submit_quiz: {str(e)}")
        print(f"[ERROR] Error type: {type(e)}")
        import traceback

        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise


@router.put(
    "/{quiz_id}",
    response_model=QuizResponse,
    responses={
        404: {
            "description": "Quiz not found",
            "content": {"application/json": {"example": {"detail": "Quiz not found"}}},
        },
        400: {
            "description": "Invalid quiz data",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid quiz type or fields"}
                }
            },
        },
        409: {
            "description": "Quiz title already exists",
            "content": {
                "application/json": {"example": {"detail": "Quiz title already exists"}}
            },
        },
    },
)
def update_quiz(quiz_id: int, quiz: QuizUpdate, db: Session = Depends(get_db)):
    # 타입별 필드 유효성 검사
    quiz.validate_fields()

    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    # Check if title exists for another quiz
    existing_quiz = (
        db.query(Quiz).filter(Quiz.title == quiz.title, Quiz.id != quiz_id).first()
    )
    if existing_quiz:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Quiz title already exists"
        )

    for key, value in quiz.model_dump(exclude_unset=True).items():
        setattr(db_quiz, key, value)

    db.commit()
    db.refresh(db_quiz)
    return db_quiz


@router.delete(
    "/{quiz_id}",
    responses={
        404: {
            "description": "Quiz not found",
            "content": {"application/json": {"example": {"detail": "Quiz not found"}}},
        },
        200: {
            "description": "Quiz deleted",
            "content": {"application/json": {"example": {"detail": "Quiz deleted"}}},
        },
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
