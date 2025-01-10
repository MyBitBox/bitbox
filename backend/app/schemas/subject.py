from pydantic import BaseModel
from typing import Optional


class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    content_type_id: int


class SubjectCreate(SubjectBase):
    pass


class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes: True
