from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, Token
from app.core.utils import hash_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=Token,
    responses={
        409: {
            "description": "Email or Nickname already registered",
            "content": {
                "application/json": {
                    "example": {"detail": "Email(Nickname) already registered"}
                }
            },
        }
    },
)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    db_nickname = db.query(User).filter(User.nickname == user.nickname).first()
    if db_nickname:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Nickname already registered"
        )

    new_user = User(
        email=user.email, password=hash_password(user.password), nickname=user.nickname
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.email})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login")
def login():
    return {"message": "login"}


@router.post("/logout")
def logout():
    return {"message": "logout"}
