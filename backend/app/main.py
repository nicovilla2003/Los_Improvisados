from fastapi import FastAPI
from app.routers import (
    auth,
    student,
    employee,
    assignment,
    exercise,
    routine,
    progress,
    recommendation,
    stats,
)

app = FastAPI()

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(employee.router)
app.include_router(assignment.router)
app.include_router(exercise.router)
app.include_router(routine.router)
app.include_router(progress.router)
app.include_router(recommendation.router)
app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al backend de GymIcesi 🏋️‍♂️"}

@app.get("/ping")
def ping():
    return {"status": "ok"}