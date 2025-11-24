# app/routers/employee.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.security import get_current_user
from app.core.permissions import (
    is_instructor,
    is_wellbeing_coordinator,
)
from app.models.user import User
from app.models.employee import Employee
from app.models.assignment import Assignment
from app.models.area import Area
from app.schemas.trainer import TrainerOut

router = APIRouter(
    prefix="/instructors",
    tags=["Instructors"],
)

@router.get("/", response_model=list[TrainerOut])
def get_all_instructors(
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Lista TODOS los instructores.
    Solo la jefa del Área de Bienestar (admin) puede usar este endpoint.
    """

    current_user, token_data = current

    if not is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el jefe del Área de Bienestar puede ver todos los instructores.",
        )

    instructors = (
        db.query(Employee)
        .filter(Employee.employee_type == "Instructor")
        .all()
    )
    return instructors


@router.get("/by-student/{student_id}", response_model=list[TrainerOut])
def get_instructors_by_student(
    student_id: str,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Admin: ver todos los instructores asignados a UN estudiante específico.
    Usa la tabla assignments (employee_id, student_id).
    """

    current_user, token_data = current

    if not is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el jefe del Área de Bienestar puede ver los instructores de un estudiante.",
        )

    instructors = (
        db.query(Employee)
        .join(Assignment, Assignment.employee_id == Employee.id)
        .filter(
            Assignment.student_id == student_id,
            Employee.employee_type == "Instructor",
        )
        .all()
    )

    return instructors


@router.get("/my", response_model=list[TrainerOut])
def get_my_instructors(
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Estudiante: ver los instructores que tiene asignados.
    Usa assignments para buscar los employees (instructores) ligados a su student_id.
    """
    current_user, token_data = current

    if current_user.role != "STUDENT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los estudiantes pueden ver sus propios instructores.",
        )

    if not current_user.student_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no tiene student_id asociado.",
        )

    instructors = (
        db.query(Employee)
        .join(Assignment, Assignment.employee_id == Employee.id)
        .filter(
            Assignment.student_id == current_user.student_id,
            Employee.employee_type == "Instructor",
        )
        .all()
    )

    return instructors
