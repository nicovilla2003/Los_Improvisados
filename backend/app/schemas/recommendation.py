from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RecommendationBase(BaseModel):
    message: str = Field(..., description="Texto de la recomendación")
    progress_doc_id: Optional[str] = Field(
        default=None,
        description="ID del log de progreso en MongoDB que da contexto a la recomendación",
    )


class RecommendationCreate(RecommendationBase):
    student_id: str = Field(..., description="Estudiante al que se dirige la recomendación")


class RecommendationUpdate(BaseModel):
    message: Optional[str] = None
    progress_doc_id: Optional[str] = None


class RecommendationRead(RecommendationBase):
    id: int
    trainer_id: str
    student_id: str
    created_at: datetime

    class Config:
        from_attributes = True
