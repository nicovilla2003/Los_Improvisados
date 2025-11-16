# Modelo para registrar el progreso de los estudiantes en sus entrenamientos.
# Permitirá guardar los resultados por ejercicio, peso, repeticiones, etc.
# En espera de definición final.

# from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
# from app.database.connection import Base

# class Progress(Base):
#     __tablename__ = "progress"
#     id = Column(Integer, primary_key=True)
#     student_id = Column(Integer, ForeignKey("students.id"))
#     exercise_id = Column(Integer, ForeignKey("exercises.id"))
#     date = Column(DateTime)
#     weight = Column(Float)
#     reps = Column(Integer)
#     notes = Column(String)
