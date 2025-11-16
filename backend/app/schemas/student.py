from pydantic import BaseModel
from typing import Optional

# Schemas relacionados con estudiantes.


class StudentBase(BaseModel):
    """
    Campos base de un estudiante.
    Debe alinearse con la tabla 'students' definida en PostgreSQL.
    En espera de definición final del esquema.
    """
    name: str
    program: Optional[str] = None
    semester: Optional[int] = None


class StudentCreate(StudentBase):
    """
    Datos necesarios para crear un estudiante (si se permite desde la API).
    En muchos casos los estudiantes pueden venir de la BD institucional
    y esta operación no se usará.
    """
    pass


class StudentUpdate(BaseModel):
    """
    Campos editables de un estudiante.
    En espera de definición final.
    """
    name: Optional[str] = None
    program: Optional[str] = None
    semester: Optional[int] = None


class StudentRead(StudentBase):
    """
    Datos devueltos al consultar un estudiante.
    """
    id: int

    class Config:
        from_attributes = True
