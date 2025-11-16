from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base


class Program(Base):
    __tablename__ = "programs"

    code = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(40), nullable=False)
    area_code = Column(Integer, ForeignKey("areas.code"), nullable=False)
