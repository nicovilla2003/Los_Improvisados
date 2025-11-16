from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database.connection import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    # 'cardio', 'fuerza', 'movilidad'
    type = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    # 'beginner', 'intermediate', 'advanced'
    difficulty = Column(String(20), nullable=True)
    # URL de video demostrativo (YouTube, etc.)
    video_url = Column(String(255), nullable=True)
    created_by_username = Column(String(30), ForeignKey("users.username"), nullable=False)