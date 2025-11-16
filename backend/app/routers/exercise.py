from fastapi import APIRouter

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("/")
async def get_all_exercises():
    # Lista todos los ejercicios disponibles.
    pass


@router.get("/{exercise_id}")
async def get_exercise_detail(exercise_id: int):
    # Devuelve los detalles de un ejercicio específico.
    pass


@router.post("/")
async def create_exercise():
    # Crea un nuevo ejercicio.
    pass


@router.put("/{exercise_id}")
async def update_exercise(exercise_id: int):
    # Actualiza la información de un ejercicio existente.
    pass


@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: int):
    # Elimina o desactiva un ejercicio.
    pass
