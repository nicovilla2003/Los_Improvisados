from pydantic import BaseModel
from typing import Optional, List

# Schemas relacionados con rutinas y su asignación a estudiantes.


class RoutineExerciseItem(BaseModel):
    """
    Representa un ejercicio dentro de una rutina (tabla puente rutina-ejercicio).
    En espera de ajuste según la tabla intermedia 'routine_exercises'.
    """
    exercise_id: int
    sets: Optional[int] = None
    reps: Optional[int] = None
    # Se pueden agregar más campos (peso objetivo, descanso, etc.) más adelante.


class RoutineBase(BaseModel):
    """
    Información base de una rutina (plantilla).
    """
    name: str
    description: Optional[str] = None
    level: Optional[str] = None  # Ej: 'beginner', 'intermediate', 'advanced'


class RoutineCreate(RoutineBase):
    """
    Datos necesarios para crear una rutina.
    Incluye la lista de ejercicios asociados.
    """
    trainer_id: int
    exercises: List[RoutineExerciseItem] = []


class RoutineUpdate(BaseModel):
    """
    Campos que se pueden actualizar en una rutina.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    exercises: Optional[List[RoutineExerciseItem]] = None


class RoutineRead(RoutineBase):
    """
    Datos devueltos al consultar una rutina.
    """
    id: int
    trainer_id: int
    exercises: List[RoutineExerciseItem] = []

    class Config:
        from_attributes = True


class RoutineAssignRequest(BaseModel):
    """
    Datos necesarios para asignar una rutina a un estudiante.
    """
    student_id: int
    start_date: Optional[str] = None  # Se puede cambiar a datetime.date más adelante
    end_date: Optional[str] = None
