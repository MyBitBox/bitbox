from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class QuizType(enum.Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    CODING = "CODING"
    TEXT = "TEXT"


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(Enum(QuizType), nullable=False, default=QuizType.MULTIPLE_CHOICE)
    options = Column(JSON, nullable=True)
    correct_option_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    subject = relationship("Subject", back_populates="quizzes")
    answers = relationship("Answer", back_populates="quiz")
