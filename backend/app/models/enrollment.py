from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    # Clave primaria compuesta
    student_id = Column(String(15), ForeignKey("students.id"), primary_key=True)
    nrc = Column(String(10), ForeignKey("groups.nrc"), primary_key=True)

    enrollment_date = Column(Date, nullable=False)
    status = Column(String(15), nullable=False)  # Active, Passed, Failed, Withdrawn
