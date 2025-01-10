from pydantic import BaseModel
from typing import Optional


class ContentTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class ContentTypeCreate(ContentTypeBase):
    pass


class ContentTypeUpdate(ContentTypeBase):
    pass


class ContentTypeResponse(ContentTypeBase):
    id: int

    class Config:
        from_attributes = True
