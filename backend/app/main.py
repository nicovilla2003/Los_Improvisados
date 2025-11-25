from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth,
    student,
    employee,
    assignment,
    exercise,
    routine,
    routine_exercise,
    progress,
    recommendation,
    # stats,
)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(employee.router)
app.include_router(assignment.router)
app.include_router(exercise.router)
app.include_router(routine.router)
app.include_router(routine_exercise.router)
app.include_router(progress.router)
app.include_router(recommendation.router)
# app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al backend de GymIcesi 🏋️‍♂️"}

@app.get("/ping")
def ping():
    return {"status": "ok"}