from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.student import Student
from app.models.employee import Employee
from app.models.area import Area
from app.models.assignment import Assignment
from app.schemas.student import StudentOut

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# ---------- Helpers de rol / permisos ----------

def is_wellbeing_coordinator(db: Session, current_user: User) -> bool:
    """
    Devuelve True si el usuario actual es el coordinador
    del Área de Bienestar (no hardcodeamos el id 1007).
    """
    if not current_user.employee_id:
        return False

    # Buscamos un área donde el coordinator_id sea este empleado
    area = (
        db.query(Area)
        .filter(
            Area.coordinator_id == current_user.employee_id,
            Area.name == "Área de Bienestar",  # según tus inserts
        )
        .first()
    )

    return area is not None


def is_instructor(db: Session, current_user: User) -> bool:
    """
    Devuelve True si el empleado asociado al usuario es de tipo 'Instructor'.
    """
    if not current_user.employee_id:
        return False

    emp = db.query(Employee).filter(Employee.id == current_user.employee_id).first()
    if not emp:
        return False

    return emp.employee_type == "Instructor"

@router.get("/admin/all", response_model=list[StudentOut])
def get_all_students_as_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Solo permitido para la Coordinadora de Bienestar.
    """
    if not is_wellbeing_coordinator(db, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el jefe del Área de Bienestar puede ver todos los estudiantes.",
        )

    students = db.query(Student).all()
    return students


@router.get("/assigned", response_model=list[StudentOut])
def get_my_assigned_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve los estudiantes asignados al instructor actual.
    - Solo funciona si el usuario es un Instructor.
    - Usa la tabla assignments (employee_id, student_id).
    """
    # Debe ser instructor
    if not is_instructor(db, current_user) and not is_wellbeing_coordinator(db, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los instructores pueden ver sus estudiantes asignados.",
        )

    if not current_user.employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no tiene employee_id asociado.",
        )

    # join Assignment -> Student
    students = (
        db.query(Student)
        .join(Assignment, Assignment.student_id == Student.id)
        .filter(Assignment.employee_id == current_user.employee_id)
        .all()
    )

    return students



@router.get("/{student_id}", response_model=StudentOut)
def get_student_by_id(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado.",
        )

    # 1) Jefe de Bienestar -> acceso completo
    if is_wellbeing_coordinator(db, current_user):
        return student

    # 2) Estudiante -> solo su propia info
    if current_user.role == "STUDENT":
        if current_user.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes ver la información de otros estudiantes.",
            )
        return student

    # 3) Instructor -> solo si tiene asignado a este estudiante
    if is_instructor(db, current_user):
        if not current_user.employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no tiene employee_id asociado.",
            )

        assigned = (
            db.query(Assignment)
            .filter(
                Assignment.employee_id == current_user.employee_id,
                Assignment.student_id == student_id,
            )
            .first()
        )

        if not assigned:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este estudiante no está asignado a ti.",
            )
        return student

    # 4) Si no cae en ninguno (otro tipo de rol)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos para ver datos de estudiantes.",
    )

