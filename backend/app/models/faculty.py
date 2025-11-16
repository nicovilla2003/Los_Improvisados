from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

class Faculty(Base):
    __tablename__ = "faculties"

    code = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(40), nullable=False)
    location = Column(String(15), nullable=False)
    phone_number = Column(String(15), nullable=False)
    dean_id = Column(String(15), ForeignKey("employees.id"), unique=True)
