from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    option_id = Column(Integer, nullable=True)  # 객관식일 때만 사용
    is_correct = Column(Boolean, nullable=False)
    time_taken = Column(Integer, nullable=False)  # 문제를 푸는 데 걸린 시간 추가
    feedback_content = Column(Text, nullable=True)  # AI 피드백 내용 추가
    subject_id = Column(
        Integer, ForeignKey("subjects.id"), nullable=False
    )  # 주제 ID 추가
    retry_count = Column(Integer, nullable=False, default=1)  # 재시도 횟수 추가
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    content = Column(
        Text, nullable=False
    )  # 사용자의 답변 (선택한 옵션 또는 입력한 코드/텍스트)

    quiz = relationship("Quiz", back_populates="answers")
    user = relationship("User", back_populates="answers")
    subject = relationship("Subject")
