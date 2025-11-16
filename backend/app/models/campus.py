from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base


class Campus(Base):
    __tablename__ = "campuses"

    code = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(20), nullable=True)  # en el SQL no estaba NOT NULL
    city_code = Column(Integer, ForeignKey("cities.code"), nullable=False)
