from sqlalchemy import Column, String
from app.database.connection import Base

class EmployeeType(Base):
    __tablename__ = "employee_types"

    name = Column(String(30), primary_key=True, index=True, nullable=False)
