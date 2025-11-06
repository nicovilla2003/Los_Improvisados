
# Proyecto Gym Icesi

Aplicación web para que estudiantes y colaboradores de la universidad puedan:

- Registrar sus rutinas de ejercicio
- Llevar seguimiento de su progreso
- Conectarse con entrenadores
- Ver estadísticas e informes útiles

El proyecto está dividido en:

- **Backend** → API con FastAPI (Python)
- **Frontend** → Interfaz web con React
- **Database** → Scripts SQL de la base de datos de la universidad (PostgreSQL)


## Estructura del proyecto

```txt
Los_Improvisados/
│
├── backend/               # API en FastAPI (Python)
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── database/
│   ├── requirements.txt
│   ├── .env.example
│   └── venv/              # entorno virtual de Python (NO se sube a git)
│
├── frontend/              # App React
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── node_modules/      # dependencias de Node (NO se sube a git)
│
├── database/
│   ├── scripts/
│   │   ├── university_drops_postgresql.sql
│   │   ├── university_schema_postgresql.sql
│   │   ├── university_full_data_postgresql.sql
│   │   └── gym_additional_tables.sql   # tablas extra (rutinas, progreso, etc.)
│   └── README.md
│
└── docs/
    └── ...
```

## Requisitos previos

Para ejecutar el proyecto se necesitan:

* **Python 3.10+**
* **Node.js** (versión 18+ recomendado)
* **PostgreSQL** instalado localmente o en la nube
* (Opcional) Cuenta de **MongoDB Atlas** si se va a usar la parte NoSQL

---

## Backend (FastAPI)

### 1. Entrar a la carpeta del backend

Desde la raíz del proyecto:

```bash
cd backend
```

### 2. Crear el entorno virtual (solo la primera vez)

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

* **PowerShell (Windows):**

  ```bash
  venv\Scripts\Activate
  ```
* **CMD (Windows):**

  ```cmd
  venv\Scripts\activate.bat
  ```
* **Git Bash / Mac / Linux:**

  ```bash
  source venv/bin/activate
  ```

Si se ve algo así, está bien:

```txt
(venv) C:\...\Los_Improvisados\backend>
```

### 4. Instalar dependencias del backend

```bash
pip install -r requirements.txt
```

#### ¿Qué paquetes se instalan?

| Paquete             | Para qué sirve                                                           |
| ------------------- | ------------------------------------------------------------------------ |
| `fastapi`           | Framework principal del backend (API), parecido a Django REST.           |
| `uvicorn`           | Servidor para correr FastAPI (`uvicorn app.main:app --reload`).          |
| `sqlalchemy`        | ORM para trabajar con PostgreSQL (modelos/tablas).                       |
| `psycopg2-binary`   | Conector entre Python y PostgreSQL.                                      |
| `python-dotenv`     | Leer variables desde un archivo `.env`.                                  |
| `pydantic`          | Validación de datos y modelos de entrada/salida.                         |
| `pymongo` / `motor` | Conectar con MongoDB (parte NoSQL).                                      |
| `passlib[bcrypt]`   | Encriptar contraseñas (si manejamos usuarios).                           |
| `requests`          | Hacer peticiones HTTP a otros servicios.                                 |
| `jinja2`            | Motor de plantillas (si en algún momento se necesitan vistas generadas). |

### 5. Variables de entorno

Copiar el archivo `.env.example` a `.env`:

```bash
cp .env.example .env   # En Windows PowerShell puede ser: copy .env.example .env
```

Editar `.env` con los datos locales de la base de datos:

```env
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=1234
PG_DATABASE=university_db

MONGO_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/gymicesi
MONGO_DB=gymicesi
```

*(Si no se va a usar Mongo aún, se puede dejar en blanco o con valores dummy.)*

### 6. Ejecutar el backend

Con el entorno virtual activo:

```bash
uvicorn app.main:app --reload
```

* API corriendo en: `http://127.0.0.1:8000`
* Documentación interactiva: `http://127.0.0.1:8000/docs`

---

##  Frontend (React)

El frontend se creó con `create-react-app` dentro de la carpeta `frontend`.

### 1. Entrar a la carpeta del frontend

Desde la raíz del proyecto:

```bash
cd frontend
```

### 2. Instalar dependencias del frontend

>  Importante: cuando se clona el proyecto desde GitHub, la carpeta `node_modules/` **no viene incluida**, así que siempre hay que hacer este paso.

```bash
npm install
```

Este comando lee `package.json` y descarga todo lo necesario (React, react-scripts, etc.)

### 3. Ejecutar el frontend

```bash
npm start
```

Esto abre la app en:

 `http://localhost:3000`

La app de React hablará con el backend (FastAPI) por HTTP, normalmente a través de URLs como `http://localhost:8000/api/...` (cuando definamos los endpoints).

---

##  Base de datos (PostgreSQL)

En la carpeta `database/scripts/` están los archivos necesarios.

Orden recomendado para ejecutar en PostgreSQL:

1. Borrar tablas existentes (si hace falta):

   ```sql
   university_drops_postgresql.sql
   ```
2. Crear las tablas base de la universidad:

   ```sql
   university_schema_postgresql.sql
   ```
3. Insertar los datos de ejemplo:

   ```sql
   university_full_data_postgresql.sql
   ```
4. Crear tablas adicionales para el proyecto (rutinas, progreso, estadísticas):

   ```sql
   gym_additional_tables.sql
   ```

Esto se puede hacer con:

* **pgAdmin**, importando cada `.sql`, o
* Desde terminal con `psql`:

```bash
psql -U postgres -d university_db -f university_schema_postgresql.sql
```

*(Los nombres reales de usuario/base pueden variar según la máquina de cada uno.)*

---

##  Cómo ejecutar todo junto

1. **Ejecutar backend**

   ```bash
   cd backend
   venv\Scripts\Activate        # o el comando equivalente en tu Sistema Operativo
   uvicorn app.main:app --reload
   ```

2. **Ejecutar frontend** (en otra terminal)

   ```bash
   cd frontend
   npm start
   ```

* Frontend: `http://localhost:3000`
* Backend: `http://127.0.0.1:8000`
* Docs backend: `http://127.0.0.1:8000/docs`

---

Cualquier cosa rara que salga en la terminal, lo primero es revisar:

* ¿Estoy en la carpeta correcta? (`backend` o `frontend`)
* ¿Tengo activo el entorno correcto? (`(venv)` en backend)
* ¿Ya corrí `pip install -r requirements.txt` (backend) o `npm install` (frontend)?
