from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    exisiting_user = db.query(User).filter(User.email == user_in.email).first()
    if exisiting_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An email with this account already exists."
        )

    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        details="Invalid email or password",
    )

    user = db.query(User).filter(User.email == credentials.email).first()
    if user is None:
        raise invalid_credentials

    if not verify_password(credentials.password, user.hashed_password):
        return invalid_credentials

    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)
