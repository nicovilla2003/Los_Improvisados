from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido al backend de GymIcesi 🏋️‍♂️"}

@app.get("/ping")
def ping():
    return {"status": "ok"}