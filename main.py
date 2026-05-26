
from fastapi import FastAPI
from database import engine
from models import Base
from routers.user_router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)