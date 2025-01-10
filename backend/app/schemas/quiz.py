from pydantic import BaseModel
from typing import List, Optional


class QuizOption(BaseModel):
    id: int
    content: str


class QuizBase(BaseModel):
    title: str
    content: str
    options: List[QuizOption]

    class Config:
        from_attributes = True


class QuizCreate(QuizBase):
    subject_id: int
    correct_option_id: int


class QuizUpdate(QuizBase):
    pass


class QuizResponse(QuizBase):
    id: int
    subject_id: int

    class Config:
        from_attributes = True


class QuizSubmitResponse(BaseModel):
    is_correct: bool
    detail: str
