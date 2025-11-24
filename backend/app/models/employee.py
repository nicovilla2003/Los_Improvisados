from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String(15), primary_key=True, index=True, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    contract_type = Column(String(30), ForeignKey("contract_types.name"), nullable=False)
    employee_type = Column(String(30), ForeignKey("employee_types.name"), nullable=False)
    faculty_code  = Column(Integer, ForeignKey("faculties.code"), nullable=False)
    campus_code   = Column(Integer, ForeignKey("campuses.code"), nullable=False)
    birth_place_code = Column(Integer, ForeignKey("cities.code"), nullable=False)
    