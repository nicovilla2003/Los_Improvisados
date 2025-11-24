from pydantic import BaseModel


class RoutineBase(BaseModel):
    name: str
    description: str | None = None
    difficulty: str | None = None

class RoutineCreate(RoutineBase):
    pass


class RoutineOut(RoutineBase):
    id: int
    created_by_username: str

    class Config:
        from_attributes = True