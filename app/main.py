
from fastapi import FastAPI
from app.database import engine
from app.models.user_models import Base
from app.routers.user_router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)