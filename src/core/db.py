from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session,declarative_base
from .config import settings

engine = create_engine(settings.DATABASE_URL)
Base = declarative_base()

SessionFactory = sessionmaker(bind=engine)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session,Depends(get_db)]