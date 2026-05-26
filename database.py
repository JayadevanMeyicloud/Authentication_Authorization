from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings



DATABASE_URL = settings.DATABASE_URL

#create postgre sql engine(postgre connection)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

#create databse session(crud operations)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

#dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()