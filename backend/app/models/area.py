from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

class Area(Base):
    __tablename__ = "areas"

    code = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(20), nullable=False)
    faculty_code = Column(Integer, ForeignKey("faculties.code"), nullable=False)
    coordinator_id = Column(String(15), ForeignKey("employees.id"), nullable=False, unique=True)
