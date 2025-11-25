from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import is_instructor, is_wellbeing_coordinator
from app.core.security import get_current_user
from app.database.deps import get_db
from app.database.mongo import mongo_db
from app.models.assignment import Assignment
from app.models.exercise import Exercise
from app.models.routine import Routine
from app.models.student import Student
from app.models.user import User
from app.schemas.progress import ProgressLogCreate, ProgressLogRead, ProgressLogUpdate

router = APIRouter(prefix="/progress", tags=["Progress"])

progress_collection = mongo_db.get_collection("progress_logs")


def _parse_object_id(log_id: str) -> ObjectId:
    try:
        return ObjectId(log_id)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de progreso inválido.",
        )


def _ensure_student_access(
    student_id: str, current_user: User, token_data: dict | None, db: Session
) -> None:
    """Valida que el usuario autenticado pueda leer/escribir el progreso."""

    if is_wellbeing_coordinator(db, current_user, token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los administradores no gestionan progresos desde este módulo.",
        )

    if current_user.role == "STUDENT":
        if not current_user.student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no tiene un student_id asociado.",
            )
        if current_user.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes gestionar tu propio progreso.",
            )
        return

    if current_user.role == "EMPLOYEE" and is_instructor(db, current_user):
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
                detail="El estudiante no está asignado a este instructor.",
            )
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Rol no autorizado para gestionar progresos.",
    )


def _ensure_references_exist(db: Session, data: ProgressLogCreate) -> None:
    if data.student_id:
        student = db.query(Student.id).filter(Student.id == data.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado.",
            )

    exercise = db.query(Exercise.id).filter(Exercise.id == data.exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado.",
        )

    if data.routine_id is not None:
        routine = db.query(Routine.id).filter(Routine.id == data.routine_id).first()
        if not routine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rutina no encontrada.",
            )


def _serialize_log(document: dict) -> ProgressLogRead:
    return ProgressLogRead(
        id=str(document["_id"]),
        student_id=document["student_id"],
        exercise_id=document["exercise_id"],
        routine_id=document.get("routine_id"),
        performed_at=document.get("performed_at") or document.get("date"),
        reps=document.get("reps"),
        sets=document.get("sets"),
        weight_kg=document.get("weight_kg") or document.get("weight"),
        duration_seconds=document.get("duration_seconds"),
        perceived_exertion=document.get("perceived_exertion"),
        notes=document.get("notes"),
    )


def _get_log_or_404(log_id: str):
    object_id = _parse_object_id(log_id)
    document = progress_collection.find_one({"_id": object_id})
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de progreso no encontrado.",
        )
    return document


@router.get(
    "/logs/{log_id}",
    response_model=ProgressLogRead,
)
def get_progress_log(
    log_id: str,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Obtiene un log puntual de progreso."""

    current_user, token_data = current
    document = _get_log_or_404(log_id)
    _ensure_student_access(document["student_id"], current_user, token_data, db)
    return _serialize_log(document)


@router.get(
    "/students/{student_id}/logs",
    response_model=list[ProgressLogRead],
)
def list_student_progress_logs(
    student_id: str,
    exercise_id: int | None = None,
    routine_id: int | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Devuelve los registros de progreso de un estudiante con filtros opcionales."""

    current_user, token_data = current
    _ensure_student_access(student_id, current_user, token_data, db)

    filters: dict[str, object] = {"student_id": student_id}
    if exercise_id is not None:
        filters["exercise_id"] = exercise_id
    if routine_id is not None:
        filters["routine_id"] = routine_id
    if start or end:
        date_filter: dict[str, datetime] = {}
        if start:
            date_filter["$gte"] = start
        if end:
            date_filter["$lte"] = end
        filters["performed_at"] = date_filter

    documents = progress_collection.find(filters).sort("performed_at", -1)
    return [_serialize_log(doc) for doc in documents]


@router.post(
    "/logs",
    response_model=ProgressLogRead,
    status_code=status.HTTP_201_CREATED,
)
def create_progress_log(
    data: ProgressLogCreate,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Crea un nuevo log de progreso en MongoDB."""

    current_user, token_data = current

    if current_user.role == "STUDENT":
        if not current_user.student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no tiene un student_id asociado.",
            )
        data.student_id = current_user.student_id
    elif current_user.role == "EMPLOYEE" and is_instructor(db, current_user):
        if not data.student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe indicar el estudiante para crear el registro.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol no autorizado para crear progresos.",
        )

    _ensure_student_access(data.student_id, current_user, token_data, db)
    _ensure_references_exist(db, data)

    insert_data = data.model_dump(exclude_none=True)
    result = progress_collection.insert_one(insert_data)
    created = progress_collection.find_one({"_id": result.inserted_id})

    return _serialize_log(created)


@router.patch("/logs/{log_id}", response_model=ProgressLogRead)
def update_progress_log(
    log_id: str,
    data: ProgressLogUpdate,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Actualiza campos de un log de progreso existente."""

    current_user, token_data = current
    document = _get_log_or_404(log_id)
    _ensure_student_access(document["student_id"], current_user, token_data, db)

    update_fields = data.model_dump(exclude_none=True)
    if update_fields:
        progress_collection.update_one(
            {"_id": document["_id"]},
            {"$set": update_fields},
        )
        document = progress_collection.find_one({"_id": document["_id"]})

    return _serialize_log(document)


@router.delete("/logs/{log_id}", response_model=ProgressLogRead)
def delete_progress_log(
    log_id: str,
    db: Session = Depends(get_db),
    current: tuple[User, dict] = Depends(get_current_user),
):
    """Elimina un log de progreso."""

    current_user, token_data = current
    document = _get_log_or_404(log_id)
    _ensure_student_access(document["student_id"], current_user, token_data, db)

    progress_collection.delete_one({"_id": document["_id"]})
    return _serialize_log(document)
