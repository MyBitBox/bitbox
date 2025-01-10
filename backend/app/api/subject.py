from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.subject import Subject as SubjectModel
from app.schemas.subject import SubjectResponse, SubjectCreate

router = APIRouter(prefix="/api/subjects", tags=["subjects"])


@router.get("/", response_model=List[SubjectResponse])
def get_subjects(content_type_id: int, db: Session = Depends(get_db)):
    subjects = (
        db.query(SubjectModel)
        .filter(SubjectModel.content_type_id == content_type_id)
        .all()
    )
    return subjects


@router.post("/", response_model=SubjectResponse)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    db_subject = SubjectModel(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.get("/{subject_id}", response_model=SubjectResponse)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int, subject: SubjectCreate, db: Session = Depends(get_db)
):
    db_subject = db.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    for key, value in subject.dict().items():
        setattr(db_subject, key, value)
    db.commit()
    db.refresh(db_subject)
    return db_subject


@router.delete("/{subject_id}", response_model=SubjectResponse)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(db_subject)
    db.commit()
    return db_subject
