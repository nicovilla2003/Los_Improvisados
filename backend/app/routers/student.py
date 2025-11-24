from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.security import get_current_user
from app.core.permissions import (
    is_instructor,
    is_wellbeing_coordinator,
)
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

@router.get("/admin/all", response_model=list[StudentOut])
def get_all_students_as_admin(
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Solo permitido para la Coordinadora de Bienestar.
    """
    current_user, token_data = current
    if not is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el jefe del Área de Bienestar puede ver todos los estudiantes.",
        )

    students = db.query(Student).all()
    return students


@router.get("/assigned", response_model=list[StudentOut])
def get_my_assigned_students(
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Devuelve los estudiantes asignados al instructor actual.
    - Solo funciona si el usuario es un Instructor.
    - Usa la tabla assignments (employee_id, student_id).
    """

    current_user, token_data = current
    # Debe ser instructor
    if not is_instructor(db, current_user) and not is_wellbeing_coordinator(db, current_user, token_data):
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
    current: tuple[User, dict] = Depends(get_current_user),
):
    
    current_user, token_data = current

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado.",
        )

    # 1) Jefe de Bienestar -> acceso completo
    if is_wellbeing_coordinator(db, current_user, token_data):
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

