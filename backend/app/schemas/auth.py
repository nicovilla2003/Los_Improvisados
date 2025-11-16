from pydantic import BaseModel
from typing import Optional

# Schemas relacionados con autenticación y contexto de usuario.


class LoginRequest(BaseModel):
    """
    Datos recibidos cuando el usuario intenta iniciar sesión.
    En espera de definición final de campos (por ejemplo: email, password, código institucional, etc.).
    """
    username: str
    password: str  # o código, según se defina más adelante


class LoginResponse(BaseModel):
    """
    Respuesta al iniciar sesión.
    En espera de implementación: token, tipo de token y datos básicos del usuario.
    """
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str  # 'student', 'trainer', 'admin', etc.


class TokenData(BaseModel):
    """
    Información contenida dentro del token (claims principales).
    En espera de ajuste según el mecanismo de autenticación que se defina.
    """
    user_id: Optional[int] = None
    role: Optional[str] = None
