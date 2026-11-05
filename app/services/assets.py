from app.schemas import AssetCreate
from sqlalchemy.orm import Session
from app.repositories import assets as assets_repository
from app.models import Asset

class AssetAlreadyExistsError(Exception):
    pass

def create_asset(db: Session, data: AssetCreate, user_id: int) -> Asset:
    existing_asset = assets_repository.get_asset_by_symbols(db, data.coin_symbol, user_id)

    if existing_asset:
        raise AssetAlreadyExistsError

    try:
        asset = assets_repository.create(db, data, user_id)

        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(asset)

    return asset
