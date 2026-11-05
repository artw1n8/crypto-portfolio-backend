from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.schemas import UserCreate, UserRead, TokenResponse
from app.services import users as users_service
from app.tokens import create_access_token
from app.models import User
from app.dependency import get_current_user

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = users_service.register_user(
            db=db,
            email=str(data.email),
            password=data.password.get_secret_value(),
        )

    except users_service.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )

    token = create_access_token(user.id)

    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse, status_code=200)
def login_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = users_service.login_user(
            db=db,
            email=str(data.email),
            password=data.password.get_secret_value(),
        )
    except users_service.InvalidCredentialsError:
         raise HTTPException(
             status_code=401,
             detail="Incorrect email or password",
         )

    token = create_access_token(user.id)

    return TokenResponse(access_token=token)

@router.get("/profile", response_model=UserRead, status_code=200)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user