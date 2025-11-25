from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class ProgressLogBase(BaseModel):
    """Campos compartidos entre las representaciones de un log de progreso."""

    exercise_id: int
    routine_id: Optional[int] = None
    performed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha y hora en la que se realizó la sesión",
    )
    reps: Optional[int] = None
    sets: Optional[int] = None
    weight_kg: Optional[float] = Field(None, description="Peso utilizado en kilogramos")
    duration_seconds: Optional[int] = Field(
        None, description="Duración total de la sesión o ejercicio en segundos"
    )
    perceived_exertion: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Nivel de esfuerzo percibido (1-10)",
    )
    notes: Optional[str] = None


class ProgressLogCreate(ProgressLogBase):
    """Datos requeridos para registrar un nuevo log en MongoDB."""

    student_id: Optional[str] = Field(
        default=None, description="Se infiere del token si el usuario es estudiante"
    )


class ProgressLogUpdate(BaseModel):
    """Campos editables en un log de progreso existente."""

    performed_at: Optional[datetime] = None
    reps: Optional[int] = None
    sets: Optional[int] = None
    weight_kg: Optional[float] = None
    duration_seconds: Optional[int] = None
    perceived_exertion: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None


class ProgressLogRead(ProgressLogBase):
    """Representación pública de un log guardado."""

    id: str
    student_id: str

    class Config:
        from_attributes = True
