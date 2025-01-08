from fastapi import FastAPI
from app.api import auth, quiz, user, content_type, subject
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 환경에서는 접근 가능한 origin으로 설정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(user.router)
app.include_router(content_type.router)
app.include_router(subject.router)
