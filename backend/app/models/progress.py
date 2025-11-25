"""Representación relacional (referencial) de los logs de progreso.

La aplicación guarda los logs de progreso en MongoDB, pero este modelo se
mantiene como espejo para analítica o herramientas de documentación.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(15), ForeignKey("students.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=True)
    performed_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    weight_kg = Column(Float, nullable=True)
    reps = Column(Integer, nullable=True)
    sets = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    perceived_exertion = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    student = relationship("Student")
    exercise = relationship("Exercise")
    routine = relationship("Routine")
