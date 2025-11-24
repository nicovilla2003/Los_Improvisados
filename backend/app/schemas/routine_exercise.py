# app/schemas/routine_exercise.py
from pydantic import BaseModel


class RoutineExerciseBase(BaseModel):
    order_index: int | None = None
    sets: int | None = None
    reps: int | None = None
    duration_seconds: int | None = None


class RoutineExerciseCreate(RoutineExerciseBase):
    routine_id: int
    exercise_id: int


class RoutineExerciseOut(RoutineExerciseBase):
    id: int
    routine_id: int
    exercise_id: int

    class Config:
        from_attributes = True  # equivale a orm_mode=True
