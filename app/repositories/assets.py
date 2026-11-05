from app.schemas import AssetCreate, AssetRead
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Asset

def get_asset_by_symbols(db: Session, coin_symbol: str, user_id: int) -> Asset | None:
    return db.scalar(select(Asset).where(Asset.user_id == user_id, Asset.coin_symbol == coin_symbol))

def create(db: Session, data: AssetCreate, user_id: int) -> Asset:
    asset = Asset(
        coin_symbol= data.coin_symbol,
        amount= data.amount,
        buy_price = data.buy_price,
        buy_date = data.buy_date,
        user_id = user_id
    )

    db.add(asset)
    db.flush()

    return asset


