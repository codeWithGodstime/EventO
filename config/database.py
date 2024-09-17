from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import get_settings
from typing import Generator

settings = get_settings()

engine = create_engine(settings.DATABASE_URI)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)

Base = declarative_base()

def get_db() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

