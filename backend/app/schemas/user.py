from pydantic import BaseModel
from typing import Optional

# Schemas genéricos para usuarios (si se maneja un modelo base de usuario).


class UserBase(BaseModel):
    """
    Información básica compartida por cualquier tipo de usuario.
    En espera de ajuste según la estructura final.
    """
    name: str
    email: str
    role: str  # 'student', 'trainer', 'admin', etc.


class UserRead(UserBase):
    """
    Datos devueltos al consultar un usuario.
    """
    id: int

    class Config:
        from_attributes = True  # Permite convertir desde objetos ORM
