# app/schemas/progress.py
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class ProgressLogBase(BaseModel):
    """
    Campos comunes de un log de progreso.
    Se refieren SIEMPRE a un solo ejercicio dentro de una rutina.
    """

    exercise_id: int
    routine_id: Optional[int] = Field(
        default=None, description="ID de la rutina (Postgres) a la que pertenece"
    )
    routine_exercise_id: Optional[int] = Field(
        default=None,
        description="ID de la tupla ROUTINE_EXERCISES (Postgres) asociada",
    )

    # Cuándo se realizó
    date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha y hora en la que se realizó el ejercicio",
    )

    # Lo que REALMENTE hizo el estudiante
    completed_sets: Optional[int] = Field(
        default=None, description="Series completadas"
    )
    completed_reps: Optional[int] = Field(
        default=None, description="Repeticiones por serie realizadas"
    )
    completed_duration_seconds: Optional[int] = Field(
        default=None,
        description="Duración total realizada en segundos (cardio/tiempo)",
    )

    weight_kg: Optional[float] = Field(
        default=None,
        description="Peso utilizado en kilogramos (si aplica)",
    )
    perceived_exertion: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Esfuerzo percibido (1-10)",
    )
    notes: Optional[str] = Field(
        default=None,
        description="Notas libres del estudiante o instructor",
    )


class ProgressLogCreate(ProgressLogBase):
    """
    Datos requeridos para crear un nuevo log.
    - student_id se infiere del token si el usuario es STUDENT.
    """

    student_id: Optional[str] = Field(
        default=None,
        description="ID del estudiante (se infiere del token si el usuario es STUDENT)",
    )


class ProgressLogUpdate(BaseModel):
    """Campos editables en un log existente (PATCH)."""

    date: Optional[datetime] = None
    completed_sets: Optional[int] = None
    completed_reps: Optional[int] = None
    completed_duration_seconds: Optional[int] = None
    weight_kg: Optional[float] = None
    perceived_exertion: Optional[int] = Field(default=None, ge=1, le=10)
    notes: Optional[str] = None


class ProgressLogRead(ProgressLogBase):
    """
    Representación pública de un log guardado en Mongo.
    """

    id: str
    student_id: str
    trainer_username: Optional[str] = Field(
        default=None,
        description="Username del instructor que registró el progreso (si aplica)",
    )

    class Config:
        from_attributes = True
