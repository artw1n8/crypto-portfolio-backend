from app.schemas import AssetCreate, AssetRead, AssetEdit
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Asset

def get_asset_by_symbols(db: Session, coin_symbol: str, user_id: int) -> Asset | None:
    return db.scalar(select(Asset).where(Asset.user_id == user_id, Asset.coin_symbol == coin_symbol))

def get_asset_by_id(db: Session, id: int, user_id: int) -> Asset | None:
    return db.scalar(select(Asset).where(Asset.user_id == user_id, Asset.id == id))

def get_all_assets(db: Session, user_id: int) -> list[Asset] | None:
    return list(db.scalars(select(Asset).where(Asset.user_id == user_id)).all())

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

def edit(db: Session, data: AssetEdit, user_id: int) -> Asset:
    asset = db.scalar(select(Asset).where(Asset.user_id == user_id, Asset.id == data.id))

    asset.amount = data.amount
    asset.buy_price = data.buy_price
    asset.buy_date = data.buy_date

    return asset

def delete(db: Session, id: int, user_id: int) -> Asset:
    asset = db.scalar(select(Asset).where(Asset.user_id == user_id, Asset.id == id))

    db.delete(asset)

