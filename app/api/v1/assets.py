from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from app.dependency import get_current_user, get_db
from app.schemas import AssetCreate, AssetRead, AssetEdit
from sqlalchemy.orm import Session
from app.services import assets as assets_service


router = APIRouter()

@router.post("/create", response_model=AssetRead, status_code=201)
def create_asset(data: AssetCreate,
                 current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        asset = assets_service.create_asset(
            db=db,
            data=data,
            user_id = current_user.id
        )

    except assets_service.AssetAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Asset with this coin already exists",
        )

    return asset

@router.post("/edit", response_model=AssetRead, status_code=200)
def edit_asset(data: AssetEdit,
               current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        asset = assets_service.edit_asset(
            db=db,
            data=data,
            user_id=current_user.id
        )

    except assets_service.AssetNotExistsError:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

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
def get_asset(id: int,
               current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        asset = assets_service.get_asset(
            db=db,
            id=id,
            user_id=current_user.id
        )

    except assets_service.AssetNotExistsError:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

    return asset

@router.get("/getall", response_model=list[AssetRead], status_code=200)
def get_all_assets(current_user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    try:
        assets = assets_service.get_all_assets(
            db=db,
            user_id=current_user.id
        )

    except assets_service.AssetNotExistsError:
        raise HTTPException(
            status_code=404,
            detail="Assets not found",
        )

    return assets