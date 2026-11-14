from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependency import get_current_user
from app.models import User
from app.dependency import get_db
from app.services import market_data as market_data_service


router = APIRouter()

@router.get("/coins")
async def get_coin_list(
    current_user: User = Depends(get_current_user),
):
    return await market_data_service.get_coin_list()