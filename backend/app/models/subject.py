from sqlalchemy import Column, String, Integer, ForeignKey
from app.database.connection import Base

class Subject(Base):
    __tablename__ = "subjects"

    code = Column(String(10), primary_key=True, index=True, nullable=False)
    name = Column(String(30), nullable=False)
    program_code = Column(Integer, ForeignKey("programs.code"), nullable=False)
