from pydantic import BaseModel
from typing import Optional

# Schemas relacionados con ejercicios.


class ExerciseBase(BaseModel):
    """
    Información base de un ejercicio.
    En espera de alinearse con la tabla 'exercises'.
    """
    name: str
    muscle_group: Optional[str] = None
    description: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    """
    Datos necesarios para crear un ejercicio.
    """
    pass


class ExerciseUpdate(BaseModel):
    """
    Campos editables de un ejercicio.
    """
    name: Optional[str] = None
    muscle_group: Optional[str] = None
    description: Optional[str] = None


class ExerciseRead(ExerciseBase):
    """
    Datos devueltos al consultar un ejercicio.
    """
    id: int

    class Config:
        from_attributes = True
