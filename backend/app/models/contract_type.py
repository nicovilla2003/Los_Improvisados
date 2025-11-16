from sqlalchemy import Column, String
from app.database.connection import Base

class ContractType(Base):
    __tablename__ = "contract_types"

    name = Column(String(30), primary_key=True, index=True, nullable=False)
