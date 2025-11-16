from fastapi import APIRouter

router = APIRouter(prefix="/routines", tags=["Routines"])

@router.get("/")
async def get_all_routines():
    # Lista todas las rutinas disponibles.
    pass


@router.get("/{routine_id}")
async def get_routine_detail(routine_id: int):
    # Devuelve los detalles de una rutina específica.
    pass


@router.post("/")
async def create_routine():
    # Crea una nueva rutina con ejercicios asociados.
    pass


@router.put("/{routine_id}")
async def update_routine(routine_id: int):
    # Actualiza una rutina existente.
    pass


@router.delete("/{routine_id}")
async def delete_routine(routine_id: int):
    # Elimina o desactiva una rutina.
    pass


@router.post("/{routine_id}/assign")
async def assign_routine_to_student(routine_id: int):
    # Asigna una rutina existente a un estudiante.
    pass
