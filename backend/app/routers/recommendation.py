from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import is_instructor, is_wellbeing_coordinator
from app.core.security import get_current_user
from app.database.deps import get_db
from app.models.assignment import Assignment
from app.models.recommendation import Recommendation
from app.models.user import User
from app.schemas.recommendation import (
    RecommendationCreate,
    RecommendationRead,
    RecommendationUpdate,
)

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def _ensure_instructor_assignment(
    trainer_id: str, student_id: str, db: Session
) -> None:
    assigned = (
        db.query(Assignment)
        .filter(
            Assignment.employee_id == trainer_id,
            Assignment.student_id == student_id,
        )
        .first()
    )
    if not assigned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El estudiante no está asignado a este instructor.",
        )


def _ensure_visibility(student_id: str, current_user: User, token_data: dict, db: Session):
    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no gestionan recomendaciones.",
        )

    if current_user.role == "STUDENT":
        if current_user.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes consultar tus recomendaciones.",
            )
        return

    if current_user.role == "EMPLOYEE" and is_instructor(db, current_user):
        _ensure_instructor_assignment(current_user.employee_id, student_id, db)
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Rol no autorizado para gestionar recomendaciones.",
    )


def _ensure_author(rec: Recommendation, current_user: User) -> None:
    if rec.trainer_id != current_user.employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el instructor autor puede modificar esta recomendación.",
        )


@router.get(
    "/students/{student_id}",
    response_model=list[RecommendationRead],
)
def list_recommendations_by_student(
    student_id: str,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Devuelve las recomendaciones asociadas a un estudiante."""

    current_user, token_data = current
    _ensure_visibility(student_id, current_user, token_data, db)

    recs = (
        db.query(Recommendation)
        .filter(Recommendation.student_id == student_id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )
    return recs


@router.get("/{recommendation_id}", response_model=RecommendationRead)
def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Obtiene una recomendación puntual si el usuario tiene acceso."""

    current_user, token_data = current

    rec = (
        db.query(Recommendation)
        .filter(Recommendation.id == recommendation_id)
        .first()
    )
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recomendación no encontrada.",
        )

    _ensure_visibility(rec.student_id, current_user, token_data, db)
    return rec


@router.post(
    "/",
    response_model=RecommendationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_recommendation(
    data: RecommendationCreate,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Crea una recomendación para un estudiante asignado."""

    current_user, token_data = current

    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no pueden crear recomendaciones.",
        )

    if not (current_user.role == "EMPLOYEE" and is_instructor(db, current_user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo instructores pueden crear recomendaciones.",
        )

    trainer_id = current_user.employee_id
    _ensure_instructor_assignment(trainer_id, data.student_id, db)

    rec = Recommendation(
        trainer_id=trainer_id,
        student_id=data.student_id,
        message=data.message,
        progress_doc_id=data.progress_doc_id,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.patch("/{recommendation_id}", response_model=RecommendationRead)
def update_recommendation(
    recommendation_id: int,
    data: RecommendationUpdate,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Actualiza una recomendación existente (solo su autor)."""

    current_user, token_data = current

    rec = (
        db.query(Recommendation)
        .filter(Recommendation.id == recommendation_id)
        .first()
    )
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recomendación no encontrada.",
        )

    _ensure_visibility(rec.student_id, current_user, token_data, db)

    if not (current_user.role == "EMPLOYEE" and is_instructor(db, current_user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo instructores pueden editar recomendaciones.",
        )

    _ensure_author(rec, current_user)

    if data.message is not None:
        rec.message = data.message
    if data.progress_doc_id is not None:
        rec.progress_doc_id = data.progress_doc_id

    db.commit()
    db.refresh(rec)
    return rec


@router.delete("/{recommendation_id}", response_model=RecommendationRead)
def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Elimina una recomendación (solo autor)."""

    current_user, token_data = current

    rec = (
        db.query(Recommendation)
        .filter(Recommendation.id == recommendation_id)
        .first()
    )
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recomendación no encontrada.",
        )

    _ensure_visibility(rec.student_id, current_user, token_data, db)

    if not (current_user.role == "EMPLOYEE" and is_instructor(db, current_user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo instructores pueden eliminar recomendaciones.",
        )

    _ensure_author(rec, current_user)

    db.delete(rec)
    db.commit()
    return rec
