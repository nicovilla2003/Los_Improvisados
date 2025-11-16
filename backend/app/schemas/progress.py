from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schemas relacionados con registros de progreso.


class ProgressLogBase(BaseModel):
    """
    Datos base de un registro de progreso (log de entrenamiento).
    Debe alinearse con la tabla 'progress'.
    """
    student_id: int
    exercise_id: int
    routine_id: Optional[int] = None
    date: datetime
    weight: Optional[float] = None
    reps: Optional[int] = None
    notes: Optional[str] = None


class ProgressLogCreate(ProgressLogBase):
    """
    Datos necesarios para crear un nuevo registro de progreso.
    """
    pass


class ProgressLogUpdate(BaseModel):
    """
    Campos que se pueden actualizar en un registro de progreso.
    """
    date: Optional[datetime] = None
    weight: Optional[float] = None
    reps: Optional[int] = None
    notes: Optional[str] = None


class ProgressLogRead(ProgressLogBase):
    """
    Datos devueltos al consultar un registro de progreso.
    """
    id: int

    class Config:
        from_attributes = True
