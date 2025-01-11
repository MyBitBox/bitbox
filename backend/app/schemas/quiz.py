from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.quiz import QuizType


class QuizOption(BaseModel):
    id: int
    content: str


class QuizBase(BaseModel):
    title: str
    content: str
    type: QuizType = QuizType.MULTIPLE_CHOICE

    class Config:
        from_attributes = True


class MultipleChoiceQuiz(QuizBase):
    options: List[QuizOption]
    correct_option_id: int


class CodingQuiz(QuizBase):
    type: QuizType = QuizType.CODING


class TextQuiz(QuizBase):
    type: QuizType = QuizType.TEXT


class QuizCreate(BaseModel):
    subject_id: int
    title: str
    content: str
    type: QuizType = QuizType.MULTIPLE_CHOICE
    options: Optional[List[QuizOption]] = None
    correct_option_id: Optional[int] = None

    def validate_fields(self):
        if self.type == QuizType.MULTIPLE_CHOICE:
            if not self.options or not self.correct_option_id:
                raise ValueError(
                    "Multiple choice quizzes require options and correct_option_id"
                )
        elif self.type in [QuizType.CODING, QuizType.TEXT]:
            if self.options or self.correct_option_id:
                raise ValueError(
                    f"{self.type.value} quizzes should not have options or correct_option_id"
                )


class QuizUpdate(QuizBase):
    pass


class QuizResponse(QuizBase):
    id: int
    subject_id: int
    options: Optional[List[QuizOption]] = None
    correct_option_id: Optional[int] = None

    class Config:
        from_attributes = True


class QuizSubmitResponse(BaseModel):
    is_correct: bool
    detail: str
