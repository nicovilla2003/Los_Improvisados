from datetime import date
from pydantic import BaseModel


class StudentBase(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    birth_date: date
    birth_place_code: int
    campus_code: int

    class Config:
        from_attributes = True


class StudentOut(StudentBase):
    """
    Response model para estudiantes. Vacio por ahora. Se puede extender en el futuro.
    """
    pass
