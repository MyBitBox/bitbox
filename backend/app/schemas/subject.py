from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    content_type_id: int


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode: True
