from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class Country(Base):
    __tablename__ = "countries"

    code = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(20), nullable=False)
