# app/routers/routine_exercise.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.core.security import get_current_user
from app.core.permissions import (
    is_instructor,
    is_wellbeing_coordinator,
)
from app.models.user import User
from app.models.assignment import Assignment
from app.models.routine import Routine
from app.models.exercise import Exercise
from app.models.routine_exercise import RoutineExercise
from app.schemas.routine_exercise import (
    RoutineExerciseCreate,
    RoutineExerciseOut,
)

router = APIRouter(
    prefix="/routine-exercises",
    tags=["RoutineExercises"],
)


def _student_can_see_routine(db: Session, current_user: User, routine: Routine) -> bool:
    if not current_user.student_id:
        return False

    # 1) Instructores asignados al estudiante
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

    allowed_creators = set([current_user.username] + instructor_usernames)

    return routine.created_by_username in allowed_creators


@router.get(
    "/{routine_id}",
    response_model=list[RoutineExerciseOut],
)
def list_exercises_for_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Devuelve los ejercicios (vía tabla intermedia) de una rutina específica.

    - ADMIN (coordinadora bienestar): NO puede ver ninguna rutina.
    - INSTRUCTOR: solo puede ver rutinas creadas por él.
    - STUDENT: puede ver rutinas creadas por él o por sus instructores asignados.
    """
    current_user, token_data = current

    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no pueden ver rutinas ni sus ejercicios.",
        )

    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada.",
        )

    if current_user.role == "EMPLOYEE" and is_instructor(db, current_user):
        if routine.created_by_username != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes ver ejercicios de tus propias rutinas.",
            )

    elif current_user.role == "STUDENT":
        if not _student_can_see_routine(db, current_user, routine):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver los ejercicios de esta rutina.",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no autorizado para ver ejercicios de rutinas.",
        )

    routine_exercises = (
        db.query(RoutineExercise)
        .filter(RoutineExercise.routine_id == routine_id)
        .order_by(RoutineExercise.order_index)
        .all()
    )

    return routine_exercises


@router.post(
    "/",
    response_model=RoutineExerciseOut,
    status_code=status.HTTP_201_CREATED,
)
def add_exercise_to_routine(
    data: RoutineExerciseCreate,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Crea una tupla rutina-ejercicio (liga un ejercicio a una rutina).

    Reglas:
    - ADMIN: no puede.
    - Solo puede hacerlo el creador de la RUTINA y del EJERCICIO.
    - Permitido para estudiantes e instructores (según sean creadores).
    """
    current_user, token_data = current

    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no pueden modificar las rutinas.",
        )

    if current_user.role == "EMPLOYEE" and not is_instructor(db, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo instructores o estudiantes pueden modificar rutinas.",
        )
    if current_user.role not in ("STUDENT", "EMPLOYEE"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no autorizado para modificar rutinas.",
        )

    routine = db.query(Routine).filter(Routine.id == data.routine_id).first()
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada.",
        )

    exercise = db.query(Exercise).filter(Exercise.id == data.exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado.",
        )


    if routine.created_by_username != current_user.username or \
       exercise.created_by_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador de la rutina y del ejercicio puede asociarlos.",
        )

    # Evitar duplicados rutina_id + exercise_id
    existing = (
        db.query(RoutineExercise)
        .filter(
            RoutineExercise.routine_id == data.routine_id,
            RoutineExercise.exercise_id == data.exercise_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este ejercicio ya está asociado a la rutina.",
        )

    re = RoutineExercise(
        routine_id=data.routine_id,
        exercise_id=data.exercise_id,
        order_index=data.order_index,
        sets=data.sets,
        reps=data.reps,
        duration_seconds=data.duration_seconds,
    )

    db.add(re)
    db.commit()
    db.refresh(re)

    return re


@router.delete(
    "/{routine_exercise_id}",
    response_model=RoutineExerciseOut,
    status_code=status.HTTP_200_OK,
)
def delete_routine_exercise(
    routine_exercise_id: int,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """
    Elimina una tupla de la tabla ROUTINE_EXERCISES.

    Reglas:
    - ADMIN: no puede.
    - Solo el creador de la rutina y del ejercicio puede eliminar el vínculo.
    """
    current_user, token_data = current

    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no pueden modificar rutinas.",
        )

    re = (
        db.query(RoutineExercise)
        .filter(RoutineExercise.id == routine_exercise_id)
        .first()
    )
    if not re:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación rutina-ejercicio no encontrada.",
        )

    routine = db.query(Routine).filter(Routine.id == re.routine_id).first()
    exercise = db.query(Exercise).filter(Exercise.id == re.exercise_id).first()

    if not routine or not exercise:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rutina o ejercicio asociado no existe.",
        )

    if routine.created_by_username != current_user.username or \
       exercise.created_by_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador de la rutina y del ejercicio puede eliminar el vínculo.",
        )

    db.delete(re)
    db.commit()

    return re
