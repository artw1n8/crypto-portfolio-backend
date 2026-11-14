from fastapi import FastAPI
from app.api.v1.users import router as users_router
from app.api.v1.assets import router as assets_router
from app.api.v1.market_data import router as market_data_router

from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(assets_router, prefix="/api/v1", tags=["assets"])
app.include_router(market_data_router, prefix="/api/v1", tags=["market"])