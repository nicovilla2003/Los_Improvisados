from app.database.connection import SessionLocal
from app.models import country, department, city, campus, faculty, area, program, subject, group, contract_type, employee_type, student, employee, enrollment, user ,exercise, routine, routine_exercise, assignment, recommendation
from datetime import date
from app.core.security import get_password_hash

def seed_database():
    db = SessionLocal()

    countries = [
        country.Country(code=1, name="Colombia"),
    ]
    db.add_all(countries)

    db.commit()

    departments = [
        department.Department(code=1, name="Valle del Cauca", country_code=1),
        department.Department(code=2, name="Cundinamarca", country_code=1),
        department.Department(code=5, name="Antioquia", country_code=1),
        department.Department(code=8, name="Atlántico", country_code=1),
        department.Department(code=11, name="Bogotá D.C.", country_code=1)
    ]
    db.add_all(departments)

    db.commit()

    cities = [
        city.City(code=101, name="Cali", dept_code=1),
        city.City(code=102, name="Bogotá", dept_code=11),
        city.City(code=103, name="Medellín", dept_code=5),
        city.City(code=104, name="Barranquilla", dept_code=8),
        city.City(code=105, name="Soledad", dept_code=8),
    ]
    db.add_all(cities)

    db.commit()

    campuses = [
        campus.Campus(code=1, name="Campus Cali", city_code=101),
        campus.Campus(code=2, name="Campus Bogotá", city_code=102),
        campus.Campus(code=3, name="Campus Medellín", city_code=103),
        campus.Campus(code=4, name="Campus Barranquilla", city_code=104)
    ]

    db.add_all(campuses)

    employee_types = [
        employee_type.EmployeeType(name="Docente"),
        employee_type.EmployeeType(name="Administrativo"),
        employee_type.EmployeeType(name="Instructor"),
    ]
    db.add_all(employee_types)

    db.commit()

    contract_types = [
        contract_type.ContractType(name="Planta"),
        contract_type.ContractType(name="Cátedra"),
    ]
    db.add_all(contract_types)

    db.commit()

    # -- Insert Employees
    # INSERT INTO EMPLOYEES (id, first_name, last_name, email, contract_type, employee_type, faculty_code, campus_code, birth_place_code) VALUES
    # ('1001', 'Juan', 'Pérez', 'juan.perez@univcali.edu.co', 'Planta', 'Docente', 1, 1, 101),
    # ('1002', 'María', 'Gómez', 'maria.gomez@univcali.edu.co', 'Planta', 'Administrativo', 1, 2, 102),
    # ('1003', 'Carlos', 'López', 'carlos.lopez@univcali.edu.co', 'Cátedra', 'Docente', 2, 1, 103),
    # ('1004', 'Carlos', 'Mejía', 'carlos.mejia@univcali.edu.co', 'Planta', 'Docente', 1, 3, 103),
    # ('1005', 'Sandra', 'Ortiz', 'sandra.ortiz@univcali.edu.co', 'Cátedra', 'Docente', 2, 4, 104),
    # ('1006', 'Julián', 'Reyes', 'julian.reyes@univcali.edu.co', 'Planta', 'Administrativo', 2, 1, 105),
    # ('1007', 'Paula', 'Ramírez', 'paula.ramirez@univcali.edu.co', 'Planta', 'Instructor', 1,1, 101),
    # ('1008', 'Andrés', 'Castro', 'andres.castro@univcali.edu.co', 'Cátedra', 'Instructor', 1, 3,103);
    
    employees = [
        employee.Employee(
            id="1001",
            first_name="Juan",
            last_name="Pérez",
            email="juan.perez@univcali.edu.co",
            contract_type="Planta",
            employee_type="Docente",
            faculty_code=1,
            campus_code=1,
            birth_place_code=101,
        ),
        employee.Employee(
            id="1002",
            first_name="María",
            last_name="Gómez",
            email="maria.gomez@univcali.edu.co",
            contract_type="Planta",
            employee_type="Administrativo",
            faculty_code=1,
            campus_code=2,
            birth_place_code=102,
        ),
        employee.Employee(
            id="1003",
            first_name="Carlos",
            last_name="López",
            email="carlos.lopez@univcali.edu.co",
            contract_type="Cátedra",
            employee_type="Docente",
            faculty_code=2,
            campus_code=1,
            birth_place_code=103,
        ),
        employee.Employee(
            id="1004",
            first_name="Carlos",
            last_name="Mejía",
            email="carlos.mejia@univcali.edu.co",
            contract_type="Planta",
            employee_type="Docente",
            faculty_code=1,
            campus_code=3,
            birth_place_code=103,
        ),
        employee.Employee(
            id="1005",
            first_name="Sandra",
            last_name="Ortiz",
            email="sandra.ortiz@univcali.edu.co",
            contract_type="Cátedra",
            employee_type="Docente",
            faculty_code=2,
            campus_code=4,
            birth_place_code=104,
        ),
        employee.Employee(
            id="1006",
            first_name="Julián",
            last_name="Reyes",
            email="julian.reyes@univcali.edu.co",
            contract_type="Planta",
            employee_type="Administrativo",
            faculty_code=2,
            campus_code=1,
            birth_place_code=105,
        ),
        employee.Employee(
            id="1007",
            first_name="Paula",
            last_name="Ramírez",
            email="paula.ramirez@univcali.edu.co",
            contract_type="Planta",
            employee_type="Instructor",
            faculty_code=1,
            campus_code=1,
            birth_place_code=101,
        ),
        employee.Employee(
            id="1008",
            first_name="Andrés",
            last_name="Castro",
            email="andres.castro@univcali.edu.co",
            contract_type="Cátedra",
            employee_type="Instructor",
            faculty_code=1,
            campus_code=3,
            birth_place_code=103,
        ),
    ]
    db.add_all(employees)

    faculties = [
        faculty.Faculty(code=1, name="Facultad de Ciencias", location="Call3", phone_number="555-1234", dean_id="1001"),
        faculty.Faculty(code=2, name="Facultad de Ingeniería", location="Call4", phone_number="555-5678", dean_id="1002"),
    ]
    db.add_all(faculties)

    db.commit()

    areas = [
        area.Area(code=1, name="Área de Sociales", faculty_code=1, coordinator_id="1001"),
        area.Area(code=2, name="Área de Ingeniería", faculty_code=2, coordinator_id="1003"),
        area.Area(code=3, name="Área de Bienestar", faculty_code=1, coordinator_id="1007"),
    ]
    db.add_all(areas)

    db.commit()

    programs = [
        program.Program(code=1, name="Psicología", area_code=1),
        program.Program(code=2, name="Ingeniería de Sistemas", area_code=2),
    ]
    db.add_all(programs)

    db.commit()

    subjects = [
        subject.Subject(code="S101", name="Psicología General", program_code=1),
        subject.Subject(code="S102", name="Cálculo I", program_code=2),
        subject.Subject(code="S103", name="Programación", program_code=2),
        subject.Subject(code="S104", name="Estructuras de Datos", program_code=2),
        subject.Subject(code="S105", name="Bases de Datos", program_code=2),
        subject.Subject(code="S106", name="Redes de Computadores", program_code=2),
        subject.Subject(code="S107", name="Sistemas Operativos", program_code=2),
        subject.Subject(code="S108", name="Algoritmos Avanzados", program_code=2),
    ]
    db.add_all(subjects)

    db.commit()

    groups = [
        group.Group(nrc="G101", number=1, semester="2023-2", subject_code="S101", professor_id="1001"),
        group.Group(nrc="G102", number=2, semester="2023-2", subject_code="S102", professor_id="1003"),
        group.Group(nrc="G103", number=3, semester="2023-2", subject_code="S103", professor_id="1004"),
        group.Group(nrc="G104", number=4, semester="2023-2", subject_code="S105", professor_id="1005"),
        group.Group(nrc="G105", number=5, semester="2023-2", subject_code="S106", professor_id="1004"),
    ]
    db.add_all(groups)

    db.commit()

    students = [
        student.Student(
            id="2001",
            first_name="Laura",
            last_name="Hernández",
            email="laura.hernandez@univcali.edu.co",
            birth_date=date(2000, 3, 15),
            birth_place_code=101,
            campus_code=1,
        ),
        student.Student(
            id="2002",
            first_name="Pedro",
            last_name="Martínez",
            email="laura.hernandez@univcali.edu.co",
            birth_date=date(1999, 7, 22),
            birth_place_code=103,
            campus_code=1,
        ),
        student.Student(
            id="2003",
            first_name="Ana",
            last_name="Suárez",
            email="ana.suarez@univcali.edu.co",
            birth_date=date(2001, 1, 5),
            birth_place_code=102,
            campus_code=2,
        ),
        student.Student(
            id="2004",
            first_name="Luis",
            last_name="Ramírez",
            email="luis.ramirez@univcali.edu.co",
            birth_date=date(1998, 11, 30),
            birth_place_code=104,
            campus_code=3,
        ),
        student.Student(
            id="2005",
            first_name="Sofía",
            last_name="García",
            email="sofia.garcia@univcali.edu.co",
            birth_date=date(2000, 9, 12),
            birth_place_code=105,
            campus_code=2,
        ),
    ]
    db.add_all(students)

    db.commit()

    # INSERT INTO ENROLLMENTS (student_id, NRC, enrollment_date, status) VALUES
    # ('2001', 'G101', '2023-08-01', 'Active'),
    # ('2001', 'G102', '2023-08-01', 'Active'),
    # ('2002', 'G103', '2023-08-02', 'Active'),
    # ('2003', 'G103', '2023-08-02', 'Active'),
    # ('2004', 'G104', '2023-08-03', 'Withdrawn'),
    # ('2005', 'G105', '2023-08-03', 'Active');


    enrollments = [ 
        enrollment.Enrollment(student_id="2001", nrc="G101", enrollment_date= date(2023, 8, 1), status="Active"),
        enrollment.Enrollment(student_id="2001", nrc="G102", enrollment_date= date(2023, 8, 1), status="Active"),
        enrollment.Enrollment(student_id="2002", nrc="G103", enrollment_date= date(2023, 8, 2), status="Active"),
        enrollment.Enrollment(student_id="2003", nrc="G103", enrollment_date= date(2023, 8, 2), status="Active"),
        enrollment.Enrollment(student_id="2004", nrc="G104", enrollment_date= date(2023, 8, 3), status="Withdrawn"),
        enrollment.Enrollment(student_id="2005", nrc="G105", enrollment_date= date(2023, 8, 3), status="Active"),
    ]
    db.add_all(enrollments)

    db.commit()

    # -- Insert Users
    # INSERT INTO USERS (username, password_hash, role, student_id, employee_id, is_active, created_at) VALUES
    # -- Estudiantes
    # ('laura.h', 'hash_lh123', 'STUDENT', '2001', NULL, TRUE, CURRENT_TIMESTAMP),
    # ('pedro.m', 'hash_pm123', 'STUDENT', '2002', NULL, TRUE, CURRENT_TIMESTAMP),
    # ('ana.s', 'hash_as123', 'STUDENT', '2003', NULL, TRUE, CURRENT_TIMESTAMP),
    # ('luis.r', 'hash_lr123', 'STUDENT', '2004', NULL, TRUE, CURRENT_TIMESTAMP),
    # ('sofia.g', 'hash_sg123', 'STUDENT', '2005', NULL, TRUE, CURRENT_TIMESTAMP),
    # -- Empleados (profesores y administrativos)
    # ('juan.p', 'hash_jp123', 'EMPLOYEE', NULL, '1001', TRUE, CURRENT_TIMESTAMP),
    # ('maria.g', 'hash_mg123', 'EMPLOYEE', NULL, '1002', TRUE, CURRENT_TIMESTAMP),
    # ('carlos.l', 'hash_cl123', 'EMPLOYEE', NULL, '1003', TRUE, CURRENT_TIMESTAMP),
    # ('carlos.m', 'hash_cm123', 'EMPLOYEE', NULL, '1004', TRUE, CURRENT_TIMESTAMP),
    # ('sandra.o', 'hash_so123', 'EMPLOYEE', NULL, '1005', TRUE, CURRENT_TIMESTAMP),
    # ('paula.r', 'hash_pr123', 'EMPLOYEE', NULL, '1007', TRUE, CURRENT_TIMESTAMP),
    # ('andres.c', 'hash_ac123', 'EMPLOYEE', NULL, '1008', TRUE, CURRENT_TIMESTAMP);

    users = [
        # Estudiantes
        user.User(username="laura.h", password_hash=get_password_hash("hash_lh123"), role="STUDENT", student_id="2001", is_active=True),
        user.User(username="pedro.m", password_hash=get_password_hash("hash_pm123"), role="STUDENT", student_id="2002", is_active=True),
        user.User(username="ana.s", password_hash=get_password_hash("hash_as123"), role="STUDENT", student_id="2003", is_active=True),
        user.User(username="luis.r", password_hash=get_password_hash("hash_lr123"), role="STUDENT", student_id="2004", is_active=True),
        user.User(username="sofia.g", password_hash=get_password_hash("hash_sg123"), role="STUDENT", student_id="2005", is_active=True),
        # Empleados
        user.User(username="juan.p", password_hash=get_password_hash("hash_jp123"), role="EMPLOYEE", employee_id="1001", is_active=True),
        user.User(username="maria.g", password_hash=get_password_hash("hash_mg123"), role="EMPLOYEE", employee_id="1002", is_active=True),
        user.User(username="carlos.l", password_hash=get_password_hash("hash_cl123"), role="EMPLOYEE", employee_id="1003", is_active=True),
        user.User(username="carlos.m", password_hash=get_password_hash("hash_cm123"), role="EMPLOYEE", employee_id="1004", is_active=True),
        user.User(username="sandra.o", password_hash=get_password_hash("hash_so123"), role="EMPLOYEE", employee_id="1005", is_active=True),
        user.User(username="paula.r", password_hash=get_password_hash("hash_pr123"), role="EMPLOYEE", employee_id="1007", is_active=True),
        user.User(username="andres.c", password_hash=get_password_hash("hash_ac123"), role="EMPLOYEE", employee_id="1008", is_active=True),
    ]
    db.add_all(users)

    db.commit()

  

    exercises_list = [
        exercise.Exercise(
            name="Press de banca",
            type="fuerza",
            description="Press de banca plano con barra.",
            duration_minutes=20,
            difficulty="intermediate",
            video_url="https://youtu.be/press-banca-demo",
            created_by_username="paula.r",  # EMPLOYEE user (trainer)
        ),
        exercise.Exercise(
            name="Sentadilla con barra",
            type="fuerza",
            description="Sentadilla trasera con barra.",
            duration_minutes=20,
            difficulty="intermediate",
            video_url="https://youtu.be/sentadilla-barra-demo",
            created_by_username="paula.r",
        ),
        exercise.Exercise(
            name="Trote en banda",
            type="cardio",
            description="Trote continuo en banda caminadora.",
            duration_minutes=30,
            difficulty="beginner",
            video_url="https://youtu.be/trote-banda-demo",
            created_by_username="andres.c",
        ),
        exercise.Exercise(
            name="Plancha abdominal",
            type="movilidad",
            description="Plancha isométrica para core.",
            duration_minutes=10,
            difficulty="beginner",
            video_url="https://youtu.be/plancha-demo",
            created_by_username="andres.c",
        ),
    ]
    db.add_all(exercises_list)
    db.flush()  # para que se asignen IDs a los Exercise

    routines_list = [
        routine.Routine(
            name="Fuerza full body principiantes",
            description="Rutina básica de fuerza para todo el cuerpo.",
            difficulty="beginner",
            created_by_username="paula.r",
        ),
        routine.Routine(
            name="Cardio y core",
            description="Sesión combinada de cardio moderado y trabajo de core.",
            difficulty="intermediate",
            created_by_username="andres.c",
        ),
    ]
    db.add_all(routines_list)
    db.flush()  # para obtener los IDs de las rutinas

    # Para facilitar, referenciamos por índice
    fuerza_full_body = routines_list[0]
    cardio_core = routines_list[1]

    press_banca = exercises_list[0]
    sentadilla = exercises_list[1]
    trote_banda = exercises_list[2]
    plancha = exercises_list[3]

    # === ROUTINE_EXERCISES (detalle de cada rutina) ===
    routine_exercises_list = [
        # Rutina de fuerza full body (Paula)
        routine_exercise.RoutineExercise(
            routine_id=fuerza_full_body.id,
            exercise_id=press_banca.id,
            order_index=1,
            sets=3,
            reps=10,
            duration_seconds=None,
        ),
        routine_exercise.RoutineExercise(
            routine_id=fuerza_full_body.id,
            exercise_id=sentadilla.id,
            order_index=2,
            sets=3,
            reps=10,
            duration_seconds=None,
        ),
        routine_exercise.RoutineExercise(
            routine_id=fuerza_full_body.id,
            exercise_id=plancha.id,
            order_index=3,
            sets=3,
            reps=30,  # 30 segundos
            duration_seconds=30,
        ),

        # Rutina de cardio y core (Andrés)
        routine_exercise.RoutineExercise(
            routine_id=cardio_core.id,
            exercise_id=trote_banda.id,
            order_index=1,
            sets=1,
            reps=None,
            duration_seconds=20 * 60,  # 20 minutos
        ),
        routine_exercise.RoutineExercise(
            routine_id=cardio_core.id,
            exercise_id=plancha.id,
            order_index=2,
            sets=4,
            reps=20,
            duration_seconds=40,
        ),
    ]
    db.add_all(routine_exercises_list)

    recommendations_list = [
        recommendation.Recommendation(
            trainer_id="1007",   # Paula
            student_id="2001",   # Laura
            message="Buen progreso en la rutina de fuerza. Intenta aumentar 2.5kg en press de banca la próxima semana.",
            progress_doc_id=None,
        ),
        recommendation.Recommendation(
            trainer_id="1007",
            student_id="2002",
            message="Te recomiendo mantener la técnica en sentadillas antes de subir peso.",
            progress_doc_id=None,
        ),
        recommendation.Recommendation(
            trainer_id="1008",  # Andrés
            student_id="2003",
            message="Excelente constancia en el cardio. Prueba agregar 5 minutos extra de trote suave.",
            progress_doc_id=None,
        ),
        recommendation.Recommendation(
            trainer_id="1008",
            student_id="2004",
            message="No olvides calentar bien antes de iniciar la rutina de cardio para evitar lesiones.",
            progress_doc_id=None,
        ),
    ]
    db.add_all(recommendations_list)


    # Empleados 1007 y 1008 son Instructor según los datos de EMPLOYEES.
    assignments_list = [
        # Paula (1007) con dos estudiantes
        assignment.Assignment(employee_id="1007", student_id="2001"),
        assignment.Assignment(employee_id="1007", student_id="2002"),

        # Andrés (1008) con tres estudiantes
        assignment.Assignment(employee_id="1008", student_id="2003"),
        assignment.Assignment(employee_id="1008", student_id="2004"),
        assignment.Assignment(employee_id="1008", student_id="2005"),
    ]
    db.add_all(assignments_list)


    db.commit()
    db.close()

if __name__ == "__main__":
    seed_database()
    print("Base de datos poblada con datos de prueba.")
