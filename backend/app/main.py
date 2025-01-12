from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import quiz, user, subject, content_type, auth
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
    allow_origins=[
        "https://v0-bitbox-yqzpj4kwtos.vercel.app",  # 프로덕션 프론트엔드 주소
        "https://bitbox-production.up.railway.app",  # Railway 프로덕션 백엔드 주소
        "http://localhost:5500",  # 로컬 개발 환경 주소 (포트는 프론트엔드 설정에 따라 다를 수 있음)
        "http://127.0.0.1:5500",  # 로컬 개발 환경 주소
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화
init_db()

# 라우터 등록
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(user.router)
app.include_router(subject.router)
app.include_router(content_type.router)
