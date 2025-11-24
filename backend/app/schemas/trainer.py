# app/schemas/trainer.py
from pydantic import BaseModel


class TrainerOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    employee_type: str
    faculty_code: int
    campus_code: int

    class Config:
        from_attributes = True
