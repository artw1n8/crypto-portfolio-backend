from fastapi import FastAPI
from app.api.v1.users import router as users_router
from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router, prefix="/api/v1", tags=["users"])