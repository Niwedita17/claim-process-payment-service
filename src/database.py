import logging

from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from functools import lru_cache

log = logging.getLogger("uvicorn")
DATABASE_URL = "sqlite:///./local.db"

def get_engine():
    log.info("Create the database engine....")
    return create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def init_db():
    log.info("Initializing database...")
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_session():
    log.info("Get the database session....")
    engine = get_engine()
    session = sessionmaker(
        bind=engine, autocommit=False, autoflush=False
    )
    try:
        yield session()
    finally:
        session().close()