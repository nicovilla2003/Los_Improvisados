from sqlalchemy import Column, String, Integer, ForeignKey, Date

from app.database.connection import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(String(15), primary_key=True, index=True, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    birth_place_code = Column(Integer, ForeignKey("cities.code"), nullable=False)
    campus_code = Column(Integer, ForeignKey("campuses.code"), nullable=False)
