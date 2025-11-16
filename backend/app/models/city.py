from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

class City(Base):
    __tablename__ = "cities"

    code = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(20), nullable=False)
    dept_code = Column(Integer, ForeignKey("departments.code"), nullable=False)
