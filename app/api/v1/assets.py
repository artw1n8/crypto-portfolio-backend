from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from app.dependency import get_current_user, get_db
from app.schemas import AssetCreate, AssetRead
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