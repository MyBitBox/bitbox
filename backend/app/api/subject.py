from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.subject import Subject as SubjectModel
from app.schemas.subject import SubjectResponse, SubjectCreate

router = APIRouter(prefix="/api/subjects/", tags=["subjects"])


@router.get("/", response_model=List[SubjectResponse])
def get_subjects(content_type_id: int, db: Session = Depends(get_db)):
    subjects = (
        db.query(SubjectModel)
        .filter(SubjectModel.content_type_id == content_type_id)
        .all()
    )
    return subjects


@router.post(
    "/",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            "description": "Subject already exists",
            "content": {
                "application/json": {"example": {"detail": "Subject already exists"}}
            },
        }
    },
)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    # Check if subject with same name exists in the same content type
    db_subject = (
        db.query(SubjectModel)
        .filter(
            SubjectModel.name == subject.name,
            SubjectModel.content_type_id == subject.content_type_id,
        )
        .first()
    )
    if db_subject:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Subject already exists"
        )

    db_subject = SubjectModel(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
    responses={
        404: {
            "description": "Subject not found",
            "content": {
                "application/json": {"example": {"detail": "Subject not found"}}
            },
        }
    },
)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found"
        )
    return db_subject


@router.put(
    "/{subject_id}",
    response_model=SubjectResponse,
    responses={
        404: {
            "description": "Subject not found",
            "content": {
                "application/json": {"example": {"detail": "Subject not found"}}
            },
        },
        409: {
            "description": "Subject name already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "Subject name already exists"}
                }
            },
        },
    },
)
def update_subject(
    subject_id: int, subject: SubjectCreate, db: Session = Depends(get_db)
):
    db_subject = db.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found"
        )

    # Check if the new name already exists for a different subject in the same content type
    existing_subject = (
        db.query(SubjectModel)
        .filter(
            SubjectModel.name == subject.name,
            SubjectModel.content_type_id == subject.content_type_id,
            SubjectModel.id != subject_id,
        )
        .first()
    )
    if existing_subject:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Subject name already exists"
        )

    for key, value in subject.model_dump().items():
        setattr(db_subject, key, value)
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.delete(
    "/{subject_id}",
    responses={
        404: {
            "description": "Subject not found",
            "content": {
                "application/json": {"example": {"detail": "Subject not found"}}
            },
        },
        200: {
            "description": "Subject deleted",
            "content": {"application/json": {"example": {"detail": "Subject deleted"}}},
        },
    },
)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found"
        )
    db.delete(db_subject)
    db.commit()
    return {"detail": "Subject deleted"}
