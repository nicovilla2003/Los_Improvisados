# app/schemas/exercise.py
from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: str
    type: str  # 'cardio', 'fuerza', 'movilidad'
    description: str | None = None
    duration_minutes: int | None = None
    difficulty: str | None = None  # 'beginner', 'intermediate', 'advanced'
    video_url: str | None = None   # URL opcional


class ExerciseCreate(ExerciseBase):
    """Datos necesarios para crear un ejercicio."""
    pass


class ExerciseOut(ExerciseBase):
    """Lo que devolvemos al frontend."""
    id: int
    created_by_username: str

    class Config:
        from_attributes = True  # para usar objetos ORM
