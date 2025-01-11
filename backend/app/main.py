from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import quiz, user, subject, content_type
from app.core.logging import setup_logging
from app.core.database import init_db

# 로깅 설정
setup_logging()

# FastAPI 앱 생성
app = FastAPI(
    debug=True,  # 디버그 모드 활성화
    title="BitBox API",
    description="BitBox 백엔드 API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화
init_db()

# 라우터 등록
app.include_router(quiz.router)
app.include_router(user.router)
app.include_router(subject.router)
app.include_router(content_type.router)
