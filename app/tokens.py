import os
from datetime import datetime, timezone, timedelta

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.environ["JWT_SECRET_KEY"]

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expires_at
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def get_user_id_from_token(token: str) -> int:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=ALGORITHM,
        options={"require": ["sub", "iat", "exp"]}
    )

    return int(payload["sub"])

