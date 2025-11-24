from pydantic import BaseModel


class AssignmentOut(BaseModel):
    employee_id: str
    student_id: str

    class Config:
        from_attributes = True