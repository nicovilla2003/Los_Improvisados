from fastapi import APIRouter

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("/students/{student_id}/logs")
async def get_progress_logs(student_id: int):
    # Devuelve todos los registros de progreso de un estudiante.
    pass


@router.post("/logs")
async def create_progress_log():
    # Crea un nuevo registro de progreso.
    pass


@router.put("/logs/{log_id}")
async def update_progress_log(log_id: int):
    # Actualiza un registro de progreso existente.
    pass


@router.delete("/logs/{log_id}")
async def delete_progress_log(log_id: int):
    # Elimina un registro de progreso.
    pass
