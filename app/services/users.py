from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User
from app.repositories import users as users_repository
from app.security import hash_password, verify_password

class EmailAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

def register_user(db: Session, email: str, password: str) -> User:
    existing_user = users_repository.get_by_email(db, email)

    if existing_user is not None:
        raise EmailAlreadyExistsError()

    password_hash = hash_password(password)

    try:
        user = users_repository.add(
            db=db,
            email=email,
            password_hash=password_hash,
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

    db.refresh(user)

    return user


def login_user(db: Session, email: str, password: str) -> User:
    existing_user = users_repository.get_by_email(db, email)

    if not existing_user:
        raise InvalidCredentialsError

    password_hash = users_repository.get_hash_by_email(
        db=db,
        email=email
    )

    is_password_correct = verify_password(password, password_hash)

    if not is_password_correct:
        raise InvalidCredentialsError

    return existing_user