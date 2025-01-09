from pydantic import BaseModel


class QuizBase(BaseModel):
    title: str
    content: str
    options: str


class QuizCreate(QuizBase):
    subject_id: int


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
