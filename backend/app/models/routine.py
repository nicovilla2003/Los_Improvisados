from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone

from app.database.connection import Base


class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    # Ej: 'beginner', 'intermediate', 'advanced'
    difficulty = Column(String(20), nullable=True)

    created_by_username = Column(
        String(30),
        ForeignKey("users.username"),
        nullable=False,
    )
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
