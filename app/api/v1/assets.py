from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from app.dependency import get_current_user, get_db
from app.schemas import AssetCreate, AssetRead, AssetEdit
from sqlalchemy.orm import Session
from app.services import assets as assets_service
from app.services import market_data as market_data_service

router = APIRouter()

@router.post("/create", response_model=AssetRead, status_code=201)
async def create_asset(data: AssetCreate,
                 current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        asset = assets_service.create_asset(
            db=db,
            data=data,
            user_id = current_user.id
        )

        current_price = await market_data_service.get_coin(
            coin_symbol=asset.coin_symbol
        )

        db.commit()

    except assets_service.AssetAlreadyExistsError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Asset with this coin already exists",
        )

    except market_data_service.InvalidCoinSymbolError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported coin symbol",
        )

    asset.current_price = current_price[asset.coin_symbol]["usd"]
    return asset

@router.post("/edit", response_model=AssetRead, status_code=200)
async def edit_asset(data: AssetEdit,
               current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        asset = assets_service.edit_asset(
            db=db,
            data=data,
            user_id=current_user.id
        )

        current_price = await market_data_service.get_coin(
            coin_symbol=asset.coin_symbol
        )

        db.commit()

    except assets_service.AssetNotExistsError:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

    except market_data_service.InvalidCoinSymbolError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported coin symbol",
        )

    asset.current_price = current_price[asset.coin_symbol]["usd"]
    return asset

@router.post("/delete", status_code=204)
def delete_asset(id: int,
               current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        asset = assets_service.delete_asset(
            db=db,
            id=id,
            user_id=current_user.id
        )

    except assets_service.AssetNotExistsError:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

@router.get("/get",response_model=AssetRead, status_code=200)
async def get_asset(id: int,
               current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        asset = assets_service.get_asset(
            db=db,
            id=id,
            user_id=current_user.id
        )
        current_price = await market_data_service.get_coin(
            coin_symbol=asset.coin_symbol
        )

    except assets_service.AssetNotExistsError:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

    except market_data_service.InvalidCoinSymbolError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported coin symbol",
        )

    asset.current_price = current_price[asset.coin_symbol]["usd"]
    return asset

@router.get("/getall", response_model=list[AssetRead], status_code=200)
async def get_all_assets(current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    try:
        assets = assets_service.get_all_assets(
            db=db,
            user_id=current_user.id
        )

        current_prices = await market_data_service.get_coins(
            coin_symbols=[asset.coin_symbol for asset in assets]
        )

    except assets_service.AssetNotExistsError:
        raise HTTPException(
            status_code=404,
            detail="Assets not found",
        )

    for asset in assets:
        coin_data = current_prices.get(asset.coin_symbol)
        asset.current_price = coin_data.get("usd")

    return assets