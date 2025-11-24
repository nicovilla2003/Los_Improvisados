from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.models.user import User
from app.models.employee import Employee
from app.models.area import Area
from app.core.security import (
    verify_password,
    create_access_token,
    decode_access_token,
)

from app.core.permissions import (
    is_instructor,
    is_wellbeing_coordinator,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()

WELLBEING_AREA_NAME = "Área de Bienestar"


# ======== Schemas ========

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True  # Pydantic v2 / orm_mode en v1


# ======== Helpers internos ========

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user: User | None = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    if not user.is_active:
        return None

    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login NORMAL:
    - Estudiantes: pueden iniciar sesión sin restricciones extra.
    - Empleados: solo si son de tipo 'Instructor'.
    El token incluye:
    - sub: username
    - role: rol del usuario (STUDENT / EMPLOYEE)
    - is_admin: False (aunque sea instructor)
    """
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    # Lógica según rol
    if user.role == "STUDENT":
        # Estudiante: ok
        pass
    elif user.role == "EMPLOYEE":
        # Solo se permite acceso a empleados que sean Instructor
        if not is_instructor(db, user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo instructores pueden iniciar sesión en esta plataforma.",
            )
    else:
        # Cualquier otro rol no está contemplado en el login normal
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no autorizado para este tipo de login.",
        )

    is_admin = False

    token_data = {
        "sub": user.username,
        "role": user.role,
        "is_admin": is_admin,
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=60),
    )
    return TokenResponse(access_token=access_token)


@router.post("/admin-login", response_model=TokenResponse)
def admin_login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login ESPECÍFICO para el módulo de administración.
    Solo el Jefe del Área de Bienestar puede autenticarse aquí.
    - Debe ser un usuario asociado a empleado.
    - Debe ser coordinador del Área de Bienestar.
    El token incluye is_admin=True para diferenciarlo claramente.
    """

    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    # Debe ser empleado y coordinador de bienestar
    if user.role != "EMPLOYEE" or not is_wellbeing_coordinator(db, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el jefe del Área de Bienestar puede iniciar sesión como administrador.",
        )

    token_data = {
        "sub": user.username,
        "role": user.role,
        "is_admin": True,
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=60),
    )
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserOut)
def read_me(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Endpoint protegido de ejemplo.
    Lee el token, busca el usuario y lo devuelve.
    (Aquí podrías más adelante también devolver is_admin si lo quieres en la respuesta.)
    """
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    username: str | None = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    user: User | None = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    return user
