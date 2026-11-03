from typing import Generator

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.repositories import users as users_repository
from app.tokens import get_user_id_from_token

security = HTTPBearer(auto_error=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(security),
        db: Session = Depends(get_db),
    ) -> User:

    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    token = credentials.credentials

    try:
        user_id = get_user_id_from_token(token)
    except (Exception, jwt.InvalidTokenError):
        raise unauthorized

    user = users_repository.get_by_id(db, user_id)

    if not user:
        raise unauthorized

    return user