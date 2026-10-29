from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from database import Base

class User(Base):
    __tablename__="user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

class Asset(Base):
    __tablename__="asset"
    id: Mapped[int] = mapped_column(primary_key=True)
    coin_symbol: Mapped[str] = mapped_column(unique=True, nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    buy_price: Mapped[Decimal] = mapped_column(nullable=False)
    buy_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)


class Alert(Base):
    __tablename__ = "alert"
    id: Mapped[int] = mapped_column(primary_key=True)
    coin_symbol: Mapped[str] = mapped_column(unique=True, nullable=False)
    target_price: Mapped[Decimal] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

