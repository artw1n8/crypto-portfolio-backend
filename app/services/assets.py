from app.schemas import AssetCreate, AssetEdit
from sqlalchemy.orm import Session
from app.repositories import assets as assets_repository
from app.models import Asset

class AssetAlreadyExistsError(Exception):
    pass

class AssetNotExistsError(Exception):
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


def edit_asset(db: Session, data: AssetEdit, user_id: int) -> Asset:
    existing_asset = assets_repository.get_asset_by_id(db, data.id, user_id)

    if not existing_asset:
        raise AssetNotExistsError

    try:
        asset = assets_repository.edit(db, data, user_id)

        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(asset)

    return asset

def delete_asset(db: Session, id: int, user_id: int) -> Asset:
    existing_asset = assets_repository.get_asset_by_id(db, id, user_id)

    if not existing_asset:
        raise AssetNotExistsError

    try:
        asset = assets_repository.delete(db, id, user_id)

        db.commit()
    except Exception:
        db.rollback()
        raise

def get_asset(db: Session, id: int, user_id: int) -> Asset:
    existing_asset = assets_repository.get_asset_by_id(db, id, user_id)

    if existing_asset is None:
        raise AssetNotExistsError

    return existing_asset

def get_all_assets(db: Session, user_id: int) -> list[Asset]:
    existing_assets = assets_repository.get_all_assets(db, user_id)

    if not existing_assets:
        raise AssetNotExistsError

    return existing_assets