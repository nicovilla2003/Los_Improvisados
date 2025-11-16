from sqlalchemy import Column, Integer, ForeignKey
from app.database.connection import Base


class RoutineExercise(Base):
    __tablename__ = "routine_exercises"

    id = Column(Integer, primary_key=True, index=True)

    routine_id = Column(
        Integer,
        ForeignKey("routines.id"),
        nullable=False,
    )

    exercise_id = Column(
        Integer,
        ForeignKey("exercises.id"),
        nullable=False,
    )

    # Orden dentro de la rutina (1, 2, 3, ...)
    order_index = Column(Integer, nullable=True)

    # Configuración básica del ejercicio dentro de la rutina
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    # En caso de ejercicios de tiempo (cardio/movilidad)
    duration_seconds = Column(Integer, nullable=True)
