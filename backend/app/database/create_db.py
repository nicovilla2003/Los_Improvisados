from app.database.connection import Base, engine

from app.models import country, department, city, campus
from app.models import faculty, area, program, subject, group
from app.models import contract_type, employee_type
from app.models import employee, student
from app.models import user
from app.models import enrollment
from app.models import exercise, routine
from app.models import routine_exercise
from app.models import assignment, recommendation

from datetime import date

def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")

if __name__ == "__main__":
    create_all_tables()