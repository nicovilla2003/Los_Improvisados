


DROP TABLE IF EXISTS recommendations CASCADE;
DROP TABLE IF EXISTS routine_exercises CASCADE;
DROP TABLE IF EXISTS routines CASCADE;
DROP TABLE IF EXISTS exercises CASCADE;

DROP TABLE IF EXISTS assignments CASCADE;

DROP TABLE IF EXISTS enrollments CASCADE;
DROP TABLE IF EXISTS users CASCADE;

DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS employees CASCADE;

DROP TABLE IF EXISTS employee_types CASCADE;
DROP TABLE IF EXISTS contract_types CASCADE;

DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS programs CASCADE;
DROP TABLE IF EXISTS areas CASCADE;
DROP TABLE IF EXISTS faculties CASCADE;

DROP TABLE IF EXISTS campuses CASCADE;
DROP TABLE IF EXISTS cities CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS countries CASCADE;



CREATE TABLE AREAS (
    code              INTEGER NOT NULL,
    name              VARCHAR(20) NOT NULL,
    faculty_code      INTEGER NOT NULL,
    coordinator_id    VARCHAR(15) NOT NULL
);

CREATE UNIQUE INDEX AREAS__IDX ON AREAS (coordinator_id);

ALTER TABLE AREAS ADD CONSTRAINT AREAS_PK PRIMARY KEY (code);

CREATE TABLE SUBJECTS (
    code            VARCHAR(10) NOT NULL,
    name            VARCHAR(30) NOT NULL,
    program_code    INTEGER NOT NULL
);

ALTER TABLE SUBJECTS ADD CONSTRAINT SUBJECTS_PK PRIMARY KEY (code);

CREATE TABLE CITIES (
    code       INTEGER NOT NULL,
    name       VARCHAR(20) NOT NULL,
    dept_code  INTEGER NOT NULL
);

ALTER TABLE CITIES ADD CONSTRAINT CITIES_PK PRIMARY KEY (code);

CREATE TABLE DEPARTMENTS (
    code      INTEGER NOT NULL,
    name      VARCHAR(20) NOT NULL,
    country_code INTEGER NOT NULL
);

ALTER TABLE DEPARTMENTS ADD CONSTRAINT DEPARTMENTS_PK PRIMARY KEY (code);

CREATE TABLE EMPLOYEES (
    id                  VARCHAR(15) NOT NULL,
    first_name          VARCHAR(30) NOT NULL,
    last_name           VARCHAR(30) NOT NULL,
    email               VARCHAR(30) NOT NULL,
    contract_type       VARCHAR(30) NOT NULL,
    employee_type       VARCHAR(30) NOT NULL,
    faculty_code        INTEGER NOT NULL,
    campus_code         INTEGER NOT NULL,
    birth_place_code    INTEGER NOT NULL
);

ALTER TABLE EMPLOYEES ADD CONSTRAINT EMPLOYEES_PK PRIMARY KEY (id);

CREATE TABLE FACULTIES (
    code         INTEGER NOT NULL,
    name         VARCHAR(40) NOT NULL,
    location     VARCHAR(15) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    dean_id      VARCHAR(15)
);

CREATE UNIQUE INDEX FACULTIES__IDX ON FACULTIES (dean_id);

ALTER TABLE FACULTIES ADD CONSTRAINT FACULTIES_PK PRIMARY KEY (code);

CREATE TABLE GROUPS (
    NRC VARCHAR(10),
	number          INTEGER NOT NULL,
    semester        VARCHAR(6) NOT NULL,
    subject_code    VARCHAR(10) NOT NULL,
    professor_id    VARCHAR(15) NOT NULL
);

ALTER TABLE GROUPS ADD CONSTRAINT GROUPS_PK PRIMARY KEY (NRC);

CREATE TABLE COUNTRIES (
    code  INTEGER NOT NULL,
    name  VARCHAR(20) NOT NULL
);

ALTER TABLE COUNTRIES ADD CONSTRAINT COUNTRIES_PK PRIMARY KEY (code);

CREATE TABLE PROGRAMS (
    code        INTEGER NOT NULL,
    name        VARCHAR(40) NOT NULL,
    area_code   INTEGER NOT NULL
);

ALTER TABLE PROGRAMS ADD CONSTRAINT PROGRAMS_PK PRIMARY KEY (code);

CREATE TABLE CAMPUSES (
    code       INTEGER NOT NULL,
    name       VARCHAR(20),
    city_code  INTEGER NOT NULL
);

ALTER TABLE CAMPUSES ADD CONSTRAINT CAMPUSES_PK PRIMARY KEY (code);

CREATE TABLE CONTRACT_TYPES (
    name VARCHAR(30) NOT NULL
);

ALTER TABLE CONTRACT_TYPES ADD CONSTRAINT CONTRACT_TYPES_PK PRIMARY KEY (name);

CREATE TABLE EMPLOYEE_TYPES (
    name VARCHAR(30) NOT NULL
);

ALTER TABLE EMPLOYEE_TYPES ADD CONSTRAINT EMPLOYEE_TYPES_PK PRIMARY KEY (name);

CREATE TABLE STUDENTS (
    id               VARCHAR(15) NOT NULL,
    first_name       VARCHAR(30) NOT NULL,
    last_name        VARCHAR(30) NOT NULL,
    email            VARCHAR(50) NOT NULL,
    birth_date       DATE NOT NULL,
    birth_place_code INTEGER NOT NULL,
    campus_code      INTEGER NOT NULL
);
ALTER TABLE STUDENTS ADD CONSTRAINT STUDENTS_PK PRIMARY KEY (id);

CREATE TABLE ENROLLMENTS (
    
	student_id     VARCHAR(15) NOT NULL,
	NRC VARCHAR(10),
    enrollment_date DATE NOT NULL,
    status         VARCHAR(15) NOT NULL  -- 'Active', 'Passed', 'Failed', 'Withdrawn'
);



CREATE TABLE USERS (
    username        VARCHAR(30) NOT NULL,
    password_hash   VARCHAR(100) NOT NULL,
    role            VARCHAR(20) NOT NULL,  -- e.g., 'STUDENT', 'EMPLOYEE', 'ADMIN'
    student_id      VARCHAR(15),
    employee_id     VARCHAR(15),
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE USERS ADD CONSTRAINT USERS_PK PRIMARY KEY (username);

CREATE TABLE RECOMMENDATIONS (
    id              SERIAL PRIMARY KEY,
    trainer_id      VARCHAR(15) NOT NULL,
    student_id      VARCHAR(15) NOT NULL,
    message         TEXT NOT NULL,
    progress_doc_id VARCHAR(50),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ROUTINES (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR(100) NOT NULL,
    description         TEXT,
    difficulty          VARCHAR(20),
    created_by_username VARCHAR(30) NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE EXERCISES (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR(100) NOT NULL,
    type                VARCHAR(20) NOT NULL,
    description         TEXT,
    duration_minutes    INTEGER,
    difficulty          VARCHAR(20),
    video_url           VARCHAR(255),
    created_by_username VARCHAR(30) NOT NULL
);

CREATE TABLE ROUTINE_EXERCISES (
    id               SERIAL PRIMARY KEY,
    routine_id       INTEGER NOT NULL,
    exercise_id      INTEGER NOT NULL,
    order_index      INTEGER,
    sets             INTEGER,
    reps             INTEGER,
    duration_seconds INTEGER
);

CREATE TABLE ASSIGNMENTS (
    employee_id VARCHAR(15) NOT NULL,
    student_id  VARCHAR(15) NOT NULL,
    PRIMARY KEY (employee_id, student_id)
);


-- Relaciones opcionales: un usuario puede corresponder a un estudiante o a un empleado
ALTER TABLE USERS ADD CONSTRAINT USERS_STUDENTS_FK 
    FOREIGN KEY (student_id) REFERENCES STUDENTS (id);

ALTER TABLE USERS ADD CONSTRAINT USERS_EMPLOYEES_FK 
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES (id);

-- Restricción lógica: un usuario no debe pertenecer a ambos tipos simultáneamente
ALTER TABLE USERS ADD CONSTRAINT USERS_ONE_ROLE_CHK 
    CHECK (
        (student_id IS NOT NULL AND employee_id IS NULL)
        OR (student_id IS NULL AND employee_id IS NOT NULL)
    );

ALTER TABLE RECOMMENDATIONS
    ADD CONSTRAINT RECOMMENDATIONS_TRAINER_FK
    FOREIGN KEY (trainer_id) REFERENCES EMPLOYEES(id);

ALTER TABLE RECOMMENDATIONS
    ADD CONSTRAINT RECOMMENDATIONS_STUDENT_FK
    FOREIGN KEY (student_id) REFERENCES STUDENTS(id);

ALTER TABLE ROUTINES
    ADD CONSTRAINT ROUTINES_USERS_FK
    FOREIGN KEY (created_by_username) REFERENCES USERS(username);

ALTER TABLE EXERCISES
    ADD CONSTRAINT EXERCISES_USERS_FK
    FOREIGN KEY (created_by_username) REFERENCES USERS(username);

ALTER TABLE ROUTINE_EXERCISES
    ADD CONSTRAINT ROUTINE_EXERCISES_ROUTINE_FK
    FOREIGN KEY (routine_id) REFERENCES ROUTINES(id);

ALTER TABLE ROUTINE_EXERCISES
    ADD CONSTRAINT ROUTINE_EXERCISES_EXERCISE_FK
    FOREIGN KEY (exercise_id) REFERENCES EXERCISES(id);

ALTER TABLE ASSIGNMENTS
    ADD CONSTRAINT ASSIGNMENTS_EMPLOYEE_FK
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(id);

ALTER TABLE ASSIGNMENTS
    ADD CONSTRAINT ASSIGNMENTS_STUDENT_FK
    FOREIGN KEY (student_id) REFERENCES STUDENTS(id);










-- Insert Countries
INSERT INTO COUNTRIES (code, name) VALUES
(1, 'Colombia');

-- Insert Departments
INSERT INTO DEPARTMENTS (code, name, country_code) VALUES
(1, 'Valle del Cauca', 1),
(2, 'Cundinamarca', 1),
(5, 'Antioquia', 1),
(8, 'Atlántico', 1),
(11, 'Bogotá D.C.', 1);



-- Insert Cities
INSERT INTO CITIES (code, name, dept_code) VALUES
(101, 'Cali', 1),
(102, 'Bogotá', 11),
(103, 'Medellín', 5),
(104, 'Barranquilla', 8),
(105, 'Soledad', 8);

-- Insert Faculties
INSERT INTO FACULTIES (code, name, location, phone_number, dean_id) VALUES
(1, 'Facultad de Ciencias', 'Call3', '555-1234', '1006'),
(2, 'Facultad de Ingeniería', 'Call4', '555-5678', '1002');

-- Insert Campuses
INSERT INTO CAMPUSES (code, name, city_code) VALUES
(1, 'Campus Cali', 101),
(2, 'Campus Bogotá', 102),
(3, 'Campus Medellín', 103),
(4, 'Campus Barranquilla', 104);

-- Insert Employee Types
INSERT INTO EMPLOYEE_TYPES (name) VALUES
('Docente'),
('Administrativo'), ('Instructor');

-- Insert Contract Types
INSERT INTO CONTRACT_TYPES (name) VALUES
('Planta'),
('Cátedra');

-- Insert Employees
INSERT INTO EMPLOYEES (id, first_name, last_name, email, contract_type, employee_type, faculty_code, campus_code, birth_place_code) VALUES
('1001', 'Juan', 'Pérez', 'juan.perez@univcali.edu.co', 'Planta', 'Docente', 1, 1, 101),
('1002', 'María', 'Gómez', 'maria.gomez@univcali.edu.co', 'Planta', 'Administrativo', 1, 2, 102),
('1003', 'Carlos', 'López', 'carlos.lopez@univcali.edu.co', 'Cátedra', 'Docente', 2, 1, 103),
('1004', 'Carlos', 'Mejía', 'carlos.mejia@univcali.edu.co', 'Planta', 'Docente', 1, 3, 103),
('1005', 'Sandra', 'Ortiz', 'sandra.ortiz@univcali.edu.co', 'Cátedra', 'Docente', 2, 4, 104),
('1006', 'Julián', 'Reyes', 'julian.reyes@univcali.edu.co', 'Planta', 'Administrativo', 2, 1, 105),
('1007', 'Paula', 'Ramírez', 'paula.ramirez@univcali.edu.co', 'Planta', 'Instructor', 1,1, 101),
('1008', 'Andrés', 'Castro', 'andres.castro@univcali.edu.co', 'Cátedra', 'Instructor', 1, 3,103);

-- Insert Areas
INSERT INTO AREAS (code, name, faculty_code, coordinator_id) VALUES
(1, 'Área de Sociales', 1, '1001'),
(2, 'Área de Ingeniería', 2, '1003'),
(3, 'Área de Bienestar', 1, '1007');

-- Insert Programs
INSERT INTO PROGRAMS (code, name, area_code) VALUES
(1, 'Psicología', 1),
(2, 'Ingeniería de Sistemas', 2);

-- Insert Subjects
INSERT INTO SUBJECTS (code, name, program_code) VALUES
('S101', 'Psicología General', 1),
('S102', 'Cálculo I', 2),
('S103', 'Programación', 2),
('S104', 'Estructuras de Datos', 2),
('S105', 'Bases de Datos', 2),
('S106', 'Redes de Computadores', 2),
('S107', 'Sistemas Operativos', 2),
('S108', 'Algoritmos Avanzados', 2);


-- Insert Groups (con NRC como PK)
INSERT INTO GROUPS (NRC, number, semester, subject_code, professor_id) VALUES
('G101', 1, '2023-2', 'S101', '1001'),
('G102', 2, '2023-2', 'S102', '1003'),
('G103', 3, '2023-2', 'S103', '1004'),
('G104', 4, '2023-2', 'S105', '1005'),
('G105', 5, '2023-2', 'S106', '1004');

-- Insert Students
INSERT INTO STUDENTS (id, first_name, last_name, email, birth_date, birth_place_code, campus_code) VALUES
('2001', 'Laura', 'Hernández', 'laura.hernandez@univcali.edu.co', '2000-03-15', 101, 1),
('2002', 'Pedro', 'Martínez', 'pedro.martinez@univcali.edu.co', '1999-07-22', 103, 1),
('2003', 'Ana', 'Suárez', 'ana.suarez@univcali.edu.co', '2001-01-05', 102, 2),
('2004', 'Luis', 'Ramírez', 'luis.ramirez@univcali.edu.co', '1998-11-30', 104, 3),
('2005', 'Sofía', 'García', 'sofia.garcia@univcali.edu.co', '2000-09-12', 105, 2);


-- Insert Enrollments (con FK a STUDENTS y GROUPS)
INSERT INTO ENROLLMENTS (student_id, NRC, enrollment_date, status) VALUES
('2001', 'G101', '2023-08-01', 'Active'),
('2001', 'G102', '2023-08-01', 'Active'),
('2002', 'G103', '2023-08-02', 'Active'),
('2003', 'G103', '2023-08-02', 'Active'),
('2004', 'G104', '2023-08-03', 'Withdrawn'),
('2005', 'G105', '2023-08-03', 'Active');


-- Insert Users
INSERT INTO USERS (username, password_hash, role, student_id, employee_id, is_active, created_at) VALUES
-- Estudiantes
('laura.h', '$2b$12$XCoxCnatwmAVAzeRMCl4tuzjhXisFQkaRJKxvKx/c0lF3PLUjN2O.', 'STUDENT', '2001', NULL, TRUE, CURRENT_TIMESTAMP),
('pedro.m', '$2b$12$Zmz06H8.DTntkZO7k5ZjEuvOsQVScPJvNvN/FQjY9Ua34VpFgUm8C', 'STUDENT', '2002', NULL, TRUE, CURRENT_TIMESTAMP),
('ana.s', '$2b$12$HQ.Fe971d1KsFe4NwZ23OeutWLCzTXesEbT2j8Xep5sag3iKfNU9u', 'STUDENT', '2003', NULL, TRUE, CURRENT_TIMESTAMP),
('luis.r', '$2b$12$f/8Z3tfrkh5w1FuUNJ23ben4cfZmxS8zRstg7wx5nGYQNW1qShjTy', 'STUDENT', '2004', NULL, TRUE, CURRENT_TIMESTAMP),
('sofia.g', '$2b$12$yEe9XBGD8xopRt6PMKzh4e/l2Kwx1ZjvyznEgvnBY78qfa58bbSre', 'STUDENT', '2005', NULL, TRUE, CURRENT_TIMESTAMP),

-- Empleados (profesores y administrativos)
('juan.p', '$2b$12$EgPCEDRbIKILjSol8b0S0uRyt1texB2K.4ECVCFxKFW2EDa8Kxt0u', 'EMPLOYEE', NULL, '1001', TRUE, CURRENT_TIMESTAMP),
('maria.g', '$2b$12$y.otcSfCIwFOjFbAaYSIAuVBPbqlHGER/yxpGvfgpAZujCrP3WExG', 'EMPLOYEE', NULL, '1002', TRUE, CURRENT_TIMESTAMP),
('carlos.l', '$2b$12$ZEZgGANlEOfCjEl8jI941OEVwUTb/z7vkQTf8yQ0dhkeLQZ0XDIke', 'EMPLOYEE', NULL, '1003', TRUE, CURRENT_TIMESTAMP),
('carlos.m', '$2b$12$nJA8ItOmF8qzKlB47adG7udfo3IntApX55RvdeTC61JgIEnIEMYMu', 'EMPLOYEE', NULL, '1004', TRUE, CURRENT_TIMESTAMP),
('sandra.o', '$2b$12$3nDtn2TdYBV2iRSfiAN2ZucX3Xst1Pug3x.SSNIHiws0G.974N0Lu', 'EMPLOYEE', NULL, '1005', TRUE, CURRENT_TIMESTAMP),
('paula.r', '$2b$12$7K/iIy5Et7hsNHvB/gzDxed.oiIQ1ebfrROjvIfNhbnky8AWyS/8e', 'EMPLOYEE', NULL, '1007', TRUE, CURRENT_TIMESTAMP),
('andres.c', '$2b$12$lrsSjdOLtX9mP6JkMJwe9OE/H5QqdErEUDJ.PZTv6AP1wSzKcGoAm', 'EMPLOYEE', NULL, '1008', TRUE, CURRENT_TIMESTAMP);

INSERT INTO EXERCISES (name, type, description, duration_minutes, difficulty, video_url, created_by_username) VALUES
('Press de banca', 'fuerza', 'Press de banca plano con barra.', 20, 'intermediate', 'https://youtu.be/press-banca-demo', 'paula.r'),
('Sentadilla con barra', 'fuerza', 'Sentadilla trasera con barra.', 20, 'intermediate', 'https://youtu.be/sentadilla-barra-demo', 'paula.r'),
('Trote en banda', 'cardio', 'Trote continuo en banda caminadora.', 30, 'beginner', 'https://youtu.be/trote-banda-demo', 'andres.c'),
('Plancha abdominal', 'movilidad', 'Plancha isométrica para core.', 10, 'beginner', 'https://youtu.be/plancha-demo', 'andres.c');

INSERT INTO ROUTINES (name, description, difficulty, created_by_username) VALUES
('Fuerza full body principiantes', 'Rutina básica de fuerza para todo el cuerpo.', 'beginner', 'paula.r'),
('Cardio y core', 'Sesión combinada de cardio moderado y trabajo de core.', 'intermediate', 'andres.c');


INSERT INTO ROUTINE_EXERCISES (routine_id, exercise_id, order_index, sets, reps, duration_seconds) VALUES
(1, 1, 1, 3, 10, NULL),
(1, 2, 2, 3, 10, NULL),

-- Rutina de cardio y core (Andrés)
(2, 3, 1, 1, NULL, 1200),   -- 20 minutos
(2, 4, 2, 4, 20, 40);


-- ====== INSERT INTO RECOMMENDATIONS ======
INSERT INTO RECOMMENDATIONS (trainer_id, student_id, message, progress_doc_id) VALUES
('1007', '2001', 'Buen progreso en la rutina de fuerza. Intenta aumentar 2.5kg en press de banca la próxima semana.', NULL),
('1007', '2002', 'Te recomiendo mantener la técnica en sentadillas antes de subir peso.', NULL),
('1008', '2003', 'Excelente constancia en el cardio. Prueba agregar 5 minutos extra de trote suave.', NULL),
('1008', '2004', 'No olvides calentar bien antes de iniciar la rutina de cardio para evitar lesiones.', NULL);


INSERT INTO ASSIGNMENTS (employee_id, student_id) VALUES
('1007', '2001'),
('1007', '2002'),
('1008', '2003'),
('1008', '2004'),
('1008', '2005');


-- Insert Foreign Key Constraints
ALTER TABLE STUDENTS ADD CONSTRAINT STUDENTS_CITIES_FK 
    FOREIGN KEY (birth_place_code) REFERENCES CITIES (code);

ALTER TABLE STUDENTS ADD CONSTRAINT STUDENTS_CAMPUSES_FK 
    FOREIGN KEY (campus_code) REFERENCES CAMPUSES (code);
	

ALTER TABLE AREAS ADD CONSTRAINT AREAS_EMPLOYEES_FK FOREIGN KEY (coordinator_id) REFERENCES EMPLOYEES (id);
ALTER TABLE AREAS ADD CONSTRAINT AREAS_FACULTIES_FK FOREIGN KEY (faculty_code) REFERENCES FACULTIES (code);

ALTER TABLE SUBJECTS ADD CONSTRAINT SUBJECTS_PROGRAMS_FK FOREIGN KEY (program_code) REFERENCES PROGRAMS (code);

ALTER TABLE CITIES ADD CONSTRAINT CITIES_DEPARTMENTS_FK FOREIGN KEY (dept_code) REFERENCES DEPARTMENTS (code);

ALTER TABLE DEPARTMENTS ADD CONSTRAINT DEPARTMENTS_COUNTRIES_FK FOREIGN KEY (country_code) REFERENCES COUNTRIES (code);

ALTER TABLE EMPLOYEES ADD CONSTRAINT EMPLOYEES_CONTRACT_TYPES_FK FOREIGN KEY (contract_type) REFERENCES CONTRACT_TYPES (name);
ALTER TABLE EMPLOYEES ADD CONSTRAINT EMPLOYEES_CITIES_FK FOREIGN KEY (birth_place_code) REFERENCES CITIES (code);
ALTER TABLE EMPLOYEES ADD CONSTRAINT EMPLOYEES_FACULTIES_FK FOREIGN KEY (faculty_code) REFERENCES FACULTIES (code);
ALTER TABLE EMPLOYEES ADD CONSTRAINT EMPLOYEES_CAMPUSES_FK FOREIGN KEY (campus_code) REFERENCES CAMPUSES (code);
ALTER TABLE EMPLOYEES ADD CONSTRAINT EMPLOYEES_EMPLOYEE_TYPES_FK FOREIGN KEY (employee_type) REFERENCES EMPLOYEE_TYPES (name);

ALTER TABLE FACULTIES ADD CONSTRAINT FACULTIES_EMPLOYEES_FK FOREIGN KEY (dean_id) REFERENCES EMPLOYEES (id);

ALTER TABLE GROUPS ADD CONSTRAINT GROUPS_SUBJECTS_FK FOREIGN KEY (subject_code) REFERENCES SUBJECTS (code);
ALTER TABLE GROUPS ADD CONSTRAINT GROUPS_EMPLOYEES_FK FOREIGN KEY (professor_id) REFERENCES EMPLOYEES (id);

ALTER TABLE PROGRAMS ADD CONSTRAINT PROGRAMS_AREAS_FK FOREIGN KEY (area_code) REFERENCES AREAS (code);

ALTER TABLE CAMPUSES ADD CONSTRAINT CAMPUSES_CITIES_FK FOREIGN KEY (city_code) REFERENCES CITIES (code);



ALTER TABLE ENROLLMENTS ADD CONSTRAINT ENROLLMENTS_PK 
    PRIMARY KEY (student_id, NRC);

ALTER TABLE ENROLLMENTS ADD CONSTRAINT ENROLLMENTS_STUDENTS_FK 
    FOREIGN KEY (student_id) REFERENCES STUDENTS (id);

ALTER TABLE ENROLLMENTS ADD CONSTRAINT ENROLLMENTS_GROUPS_FK 
    FOREIGN KEY (NRC) 
    REFERENCES GROUPS (NRC);
	
