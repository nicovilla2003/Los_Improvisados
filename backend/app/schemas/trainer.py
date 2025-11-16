from pydantic import BaseModel
from typing import Optional

# Schemas relacionados con entrenadores.


class TrainerBase(BaseModel):
    """
    Información básica de un entrenador.
    En espera de alinearse con la tabla 'trainers'.
    """
    name: str
    specialization: Optional[str] = None
    experience_years: Optional[int] = None


class TrainerCreate(TrainerBase):
    """
    Datos necesarios para crear un entrenador.
    """
    pass


class TrainerUpdate(BaseModel):
    """
    Campos que se pueden actualizar de un entrenador.
    """
    name: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None


class TrainerRead(TrainerBase):
    """
    Datos devueltos al consultar un entrenador.
    """
    id: int

    class Config:
        from_attributes = True
