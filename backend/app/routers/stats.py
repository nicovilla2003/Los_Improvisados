from fastapi import APIRouter

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/students/{student_id}/summary")
async def get_student_summary(student_id: int):
    # Devuelve un resumen de rendimiento general del estudiante.
    pass


@router.get("/students/{student_id}/progress-by-exercise")
async def get_progress_by_exercise(student_id: int, exercise_id: int):
    # Devuelve datos de progreso específicos por ejercicio (para gráficas).
    pass


@router.get("/trainers/{trainer_id}/students-summary")
async def get_trainer_summary(trainer_id: int):
    # Devuelve estadísticas generales de los estudiantes a cargo del entrenador.
    pass
