from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.content_type import ContentTypeResponse, ContentTypeCreate
from app.models.content_type import ContentType

router = APIRouter(prefix="/api/content_types", tags=["content_type"])


@router.get("/", response_model=List[ContentTypeResponse])
def get_content_types(db: Session = Depends(get_db)):
    return db.query(ContentType).all()


@router.post(
    "/",
    response_model=ContentTypeResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            "description": "Content type already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Content type already exists"}
                }
            },
        }
    },
)
def create_content_type(content_type: ContentTypeCreate, db: Session = Depends(get_db)):
    db_content_type = (
        db.query(ContentType).filter(ContentType.name == content_type.name).first()
    )
    if db_content_type:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Content type already exists"
        )

    new_content_type = ContentType(**content_type.model_dump())
    db.add(new_content_type)
    db.commit()
    db.refresh(new_content_type)
    return new_content_type


@router.put(
    "/{content_type_id}",
    response_model=ContentTypeResponse,
    responses={
        404: {
            "description": "Content type not found",
            "content": {
                "application/json": {"example": {"detail": "Content type not found"}}
            },
        }
    },
)
def update_content_type(
    content_type_id: int,
    content_type: ContentTypeCreate,
    db: Session = Depends(get_db),
):
    db_content_type = (
        db.query(ContentType).filter(ContentType.id == content_type_id).first()
    )
    if not db_content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content type not found"
        )

    db_content_type.name = content_type.name
    db_content_type.description = content_type.description
    db.commit()
    db.refresh(db_content_type)
    return db_content_type


@router.delete(
    "/{content_type_id}",
    responses={
        404: {
            "description": "Content type not found",
            "content": {
                "application/json": {"example": {"detail": "Content type not found"}}
            },
        },
        200: {
            "description": "Content type deleted",
            "content": {
                "application/json": {"example": {"detail": "Content type deleted"}}
            },
        },
    },
)
def delete_content_type(content_type_id: int, db: Session = Depends(get_db)):
    db_content_type = (
        db.query(ContentType).filter(ContentType.id == content_type_id).first()
    )
    if not db_content_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content type not found"
        )

    db.delete(db_content_type)
    db.commit()
    return {"detail": "Content type deleted"}
