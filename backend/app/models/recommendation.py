from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(String(15), ForeignKey("employees.id"), nullable=False)
    student_id = Column(String(15), ForeignKey("students.id"), nullable=False)
    message = Column(Text, nullable=False)
    progress_doc_id = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    trainer = relationship("Employee")
    student = relationship("Student")
