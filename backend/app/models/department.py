from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

class Department(Base):
    __tablename__ = "departments"

    code = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(20), nullable=False)
    country_code = Column(Integer, ForeignKey("countries.code"), nullable=False)
