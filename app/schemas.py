from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr, Field, field_validator, ConfigDict


class UserCreate (BaseModel):
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=72)

    @field_validator("password")
    def validate_password_length(cls, value: SecretStr) -> SecretStr:
        password = value.get_secret_value()

        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password length error")

        return value

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"