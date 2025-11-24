from pydantic import BaseModel
from typing import Optional
from datetime import date


class StudentBase(BaseModel):
    """
    Campos base de un estudiante.
    """
    id: str
    first_name: str
    last_name: str
    email: str
    birth_date: date
    birth_place_code: int
    campus_code: int


class StudentOut(StudentBase):
    """
    Datos devueltos al consultar un estudiante.
    """
    
    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    """
    Datos necesarios para crear un estudiante.
    """
    id: str
    first_name: str
    last_name: str
    email: str
    birth_date: date
    birth_place_code: int
    campus_code: int


class StudentUpdate(BaseModel):
    """
    Campos editables de un estudiante.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[date] = None
    campus_code: Optional[int] = None