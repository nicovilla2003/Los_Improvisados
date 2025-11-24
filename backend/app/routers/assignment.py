# app/routers/assignment.py
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
from app.models.student import Student
from app.models.assignment import Assignment
from app.models.area import Area
from app.schemas.assignment import AssignmentOut

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"],
)

@router.post("/", response_model=AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_assignment(
    payload: AssignmentOut,  # lo usamos como body de entrada
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Crear una asignación instructor-estudiante.
    """
    current_user, token_data = current

    if not is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el jefe del Área de Bienestar puede asignar instructores.",
        )

    # Validar que el empleado exista y sea Instructor
    emp = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado.",
        )

    if emp.employee_type != "Instructor":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden asignar empleados de tipo 'Instructor'.",
        )

    # Validar que el estudiante exista
    stu = db.query(Student).filter(Student.id == payload.student_id).first()
    if not stu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado.",
        )

    # Verificar que la asignación no exista ya
    existing = (
        db.query(Assignment)
        .filter(
            Assignment.employee_id == payload.employee_id,
            Assignment.student_id == payload.student_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta asignación ya existe.",
        )

    assignment = Assignment(
        employee_id=payload.employee_id,
        student_id=payload.student_id,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


@router.delete(
    "/{employee_id}/{student_id}",
    response_model=AssignmentOut,
    status_code=status.HTTP_200_OK,
)
def delete_assignment(
    employee_id: str,
    student_id: str,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Elimina una asignación instructor-estudiante.
    Solo el jefe del Área de Bienestar puede hacerlo.
    """
    current_user, token_data = current

    if not is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el jefe del Área de Bienestar puede eliminar asignaciones.",
        )

    assignment = (
        db.query(Assignment)
        .filter(
            Assignment.employee_id == employee_id,
            Assignment.student_id == student_id,
        )
        .first()
    )
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación no encontrada.",
        )

    db.delete(assignment)
    db.commit()

    return assignment
