# app/routers/exercise.py
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
from app.models.area import Area
from app.models.assignment import Assignment
from app.models.exercise import Exercise
from app.models.routine_exercise import RoutineExercise
from app.schemas.exercise import ExerciseOut, ExerciseCreate

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)

@router.get("/", response_model=list[ExerciseOut])
def list_exercises(
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    - STUDENT: ejercicios creados por él + por sus instructores asignados.
    - INSTRUCTOR: ejercicios creados por él.
    - ADMIN (coordinadora bienestar): no ve ninguno de los ejercicios.
    """
    current_user, token_data = current
    # Admin: no ve nada

    if not is_wellbeing_coordinator(db, current_user, token_data):

        # Instructor: solo sus ejercicios
        if current_user.role == "EMPLOYEE" and is_instructor(db, current_user):
            exercises = (
                db.query(Exercise)
                .filter(Exercise.created_by_username == current_user.username)
                .all()
            )
            return exercises

        # Estudiante: los suyos + los de sus instructores
        if current_user.role == "STUDENT":
            if not current_user.student_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario estudiante no tiene student_id asociado.",
                )

            # 1) IDs de instructores asignados
            assignments = (
                db.query(Assignment)
                .filter(Assignment.student_id == current_user.student_id)
                .all()
            )
            instructor_ids = [a.employee_id for a in assignments]

            instructor_usernames: list[str] = []
            if instructor_ids:
                instructor_users = (
                    db.query(User)
                    .filter(User.employee_id.in_(instructor_ids))
                    .all()
                )
                instructor_usernames = [u.username for u in instructor_users]

            allowed_creators = list(
                set([current_user.username] + instructor_usernames)
            )

            exercises = (
                db.query(Exercise)
                .filter(Exercise.created_by_username.in_(allowed_creators))
                .all()
            )
            return exercises

    # Cualquier otro rol no está contemplado
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Rol no autorizado para listar ejercicios.",
    )


@router.post(
    "/",
    response_model=ExerciseOut,
    status_code=status.HTTP_201_CREATED,
)
def create_exercise(
    data: ExerciseCreate,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Crear un ejercicio.
    - Permitido para: STUDENT y EMPLOYEE (Instructor).
    """
    current_user, token_data = current
    # Estudiante: permitido
    if current_user.role == "STUDENT":
        pass
    # Empleado: solo si es Instructor
    elif is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no autorizado para crear ejercicios.",
        )
    elif current_user.role == "EMPLOYEE":
        if not is_instructor(db, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los empleados instructores pueden crear ejercicios.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no autorizado para crear ejercicios.",
        )

    exercise = Exercise(
        name=data.name,
        type=data.type,
        description=data.description,
        duration_minutes=data.duration_minutes,
        difficulty=data.difficulty,
        video_url=data.video_url,
        created_by_username=current_user.username,
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise


@router.delete(
    "/{exercise_id}",
    response_model=ExerciseOut,
    status_code=status.HTTP_200_OK,
)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Borrar un ejercicio:
    - Solo el creador lo puede borrar.
    - Solo si el ejercicio NO está siendo usado en ninguna rutina.
      (para no romper rutinas existentes).
    """

    current_user, token_data = current
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado.",
        )

    # Solo el dueño puede borrar
    if exercise.created_by_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador del ejercicio puede eliminar este ejercicio.",
        )

    # Verificar si está ligado a alguna rutina
    used = (
        db.query(RoutineExercise)
        .filter(RoutineExercise.exercise_id == exercise_id)
        .first()
    )
    if used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede borrar el ejercicio porque está asociado a una rutina.",
        )

    db.delete(exercise)
    db.commit()

    return exercise
