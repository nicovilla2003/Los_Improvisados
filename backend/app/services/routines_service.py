# Lógica de negocio para rutinas de entrenamiento.

def get_all_routines(db):
    """Devuelve todas las rutinas creadas."""
    pass


def get_routine_by_id(db, routine_id: int):
    """Obtiene una rutina específica."""
    pass


def create_routine(db, routine_data):
    """Crea una nueva rutina (incluye ejercicios asociados)."""
    pass


def update_routine(db, routine_id: int, routine_data):
    """Actualiza los datos de una rutina existente."""
    pass


def delete_routine(db, routine_id: int):
    """Elimina o desactiva una rutina."""
    pass


def assign_routine_to_student(db, routine_id: int, student_id: int):
    """Asigna una rutina existente a un estudiante."""
    pass
