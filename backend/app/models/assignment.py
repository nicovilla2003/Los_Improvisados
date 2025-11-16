from sqlalchemy import Column, String, Date, DateTime, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Assignment(Base):
    __tablename__ = "assignments"

    # compuesta
    employee_id = Column(String(15), ForeignKey("employees.id"), nullable=False)
    student_id  = Column(String(15), ForeignKey("students.id"),  nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("employee_id", "student_id", name="assignments_pk"),
    )

    # Relaciones ORM para navegación
    employee = relationship("Employee")
    student  = relationship("Student")
