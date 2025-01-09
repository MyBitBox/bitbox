from pydantic import BaseModel


class ContentTypeBase(BaseModel):
    name: str
    description: str | None = None


class ContentTypeCreate(ContentTypeBase):
    pass


class ContentTypeUpdate(ContentTypeBase):
    pass


class ContentTypeResponse(ContentTypeBase):
    id: int

    class Config:
        from_attributes = True
