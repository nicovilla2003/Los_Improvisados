from fastapi import APIRouter

router = APIRouter(prefix="/trainers", tags=["Trainers"])

@router.get("/")
async def get_all_trainers():
    # Obtiene la lista de entrenadores registrados.
    pass


@router.get("/{trainer_id}")
async def get_trainer_detail(trainer_id: int):
    # Devuelve los detalles de un entrenador específico.
    pass


@router.get("/{trainer_id}/students")
async def get_trainer_students(trainer_id: int):
    # Devuelve los estudiantes asignados a un entrenador.
    pass


@router.get("/{trainer_id}/routines")
async def get_trainer_routines(trainer_id: int):
    # Devuelve las rutinas creadas o gestionadas por un entrenador.
    pass
