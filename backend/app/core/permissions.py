from sqlalchemy.orm import Session
from app.models.user import User
from app.models.employee import Employee
from app.models.area import Area

WELLBEING_AREA_NAME = "Área de Bienestar"


def is_instructor(db: Session, user: User) -> bool:
    """Retorna True si el usuario es empleado tipo Instructor."""
    if not user.employee_id:
        return False

    emp = db.query(Employee).filter(Employee.id == user.employee_id).first()
    if not emp:
        return False

    return emp.employee_type == "Instructor"


def is_wellbeing_coordinator(
    db: Session,
    user,
    token_data: dict | None = None
) -> bool:
    """
    Devuelve True si el usuario ES coordinador,
    pero respeta el modo de sesión (token is_admin).

    Prioridad:
    1) Si el token define is_admin → usar ese valor.
    2) Si no, determinar por BD si es el coordinador real.
    """

    # --- 1) Si el token trae is_admin, respetarlo ---
    if token_data and "is_admin" in token_data:
        return token_data["is_admin"]

    # --- 2) Modo tradicional: revisar si ES coordinadora en BD ---
    if not user.employee_id:
        return False

    area = (
        db.query(Area)
        .filter(
            Area.coordinator_id == user.employee_id,
            Area.name == WELLBEING_AREA_NAME,
        )
        .first()
    )

    return area is not None


def is_student(user: User) -> bool:
    return user.role == "STUDENT"


def is_employee(user: User) -> bool:
    return user.role == "EMPLOYEE"
