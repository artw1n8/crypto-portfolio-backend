from datetime import datetime
from decimal import Decimal

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



class AssetCreate (BaseModel):
    coin_symbol: str = Field(min_length=2, max_length=72)
    amount: int = Field(gt=0)
    buy_price: Decimal = Field(gt=0)
    buy_date: datetime

class AssetEdit (BaseModel):
    id: int
    amount: int = Field(gt=0)
    buy_price: Decimal = Field(gt=0)
    buy_date: datetime

class AssetRead (BaseModel):
    id: int
    coin_symbol: str = Field(min_length=2, max_length=72)
    amount: int = Field(gt=0)
    buy_price: Decimal = Field(gt=0)
    buy_date: datetime
