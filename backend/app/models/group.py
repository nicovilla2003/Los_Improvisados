from sqlalchemy import Column, String, ForeignKey, Integer
from app.database.connection import Base


class Group(Base):
    __tablename__ = "groups"

    nrc = Column(String(10), primary_key=True, index=True, nullable=False)
    number = Column(Integer, nullable=False)
    semester = Column(String(6), nullable=False)
    subject_code = Column(String(10), ForeignKey("subjects.code"), nullable=False)
    professor_id = Column(String(15), ForeignKey("employees.id"), nullable=False)
