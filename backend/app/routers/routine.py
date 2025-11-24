# app/routers/routine.py

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
from app.schemas.routine import RoutineCreate, RoutineOut

router = APIRouter(
    prefix="/routines",
    tags=["Routines"],
)


@router.get("/", response_model=list[RoutineOut])
def list_routines(
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    current_user, token_data = current

    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no pueden ver rutinas.",
        )

    if current_user.role == "EMPLOYEE" and is_instructor(db, current_user):
        routines = (
            db.query(Routine)
            .filter(Routine.created_by_username == current_user.username)
            .all()
        )
        return routines

    if current_user.role == "STUDENT":
        if not current_user.student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario estudiante sin student_id.",
            )

        
        assignments = (
            db.query(Assignment)
            .filter(Assignment.student_id == current_user.student_id)
            .all()
        )
        instructor_ids = [a.employee_id for a in assignments]

        instructor_usernames = []
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

        routines = (
            db.query(Routine)
            .filter(Routine.created_by_username.in_(allowed_creators))
            .all()
        )
        return routines

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Rol no autorizado para ver rutinas.",
    )


@router.post("/", response_model=RoutineOut, status_code=status.HTTP_201_CREATED)
def create_routine(
    data: RoutineCreate,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    current_user, token_data = current

    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no pueden crear rutinas.",
        )

    if current_user.role == "STUDENT":
        pass

    elif current_user.role == "EMPLOYEE" and is_instructor(db, current_user):
        pass

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no autorizado para crear rutinas.",
        )

    routine = Routine(
        name=data.name,
        description=data.description,
        difficulty=data.difficulty,
        created_by_username=current_user.username,
    )

    db.add(routine)
    db.commit()
    db.refresh(routine)

    return routine


@router.delete("/{routine_id}", response_model=RoutineOut)
def delete_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    current_user, token_data = current

    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rutina no encontrada.",
        )

    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no pueden borrar rutinas.",
        )

    if routine.created_by_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador de la rutina puede eliminarla.",
        )

    db.delete(routine)
    db.commit()

    return routine
