from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    """
    Provide a SQLAlchemy database session.

    Yields:
        Generator: A SessionLocal instance.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
