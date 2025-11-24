from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, student

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(student.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido al backend de GymIcesi 🏋️‍♂️"}

@app.get("/ping")
def ping():
    return {"status": "ok"}