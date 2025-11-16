from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, CheckConstraint
from datetime import datetime, timezone

from app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String(30), primary_key=True, index=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # e.g. 'STUDENT', 'EMPLOYEE', 'ADMIN'

    # FKs opcionales: pueden apuntar a Student o a Employee
    student_id = Column(
        String(15),
        ForeignKey("students.id"),
        nullable=True,
    )
    employee_id = Column(
        String(15),
        ForeignKey("employees.id"),
        nullable=True,
    )

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        # Restricción lógica: el usuario debe ser estudiante O empleado, pero no ambos a la vez
        CheckConstraint(
            "((student_id IS NOT NULL AND employee_id IS NULL) "
            "OR (student_id IS NULL AND employee_id IS NOT NULL))",
            name="users_one_role_chk",
        ),
    )
