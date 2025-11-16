# backend/app/database/deps.py
from typing import Generator
from .connection import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
