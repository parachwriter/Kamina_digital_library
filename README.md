# Kamina Digital Library
API REST para gestión de biblioteca digital con FastAPI

## Funciones del proyecto 
- Suite de Pruebas Unitarias utilizando **pytest**, incluyendo **mocks**
- Gestión completa (CRUD) de **Usuarios, Autores y Libros**

- Función de **búsqueda** de libros por título, autor o fecha de publicación

- Control de **préstamos** y retornos de ejemplares

- Sistema de autenticación basado en JWT

- Generación automática de documentación con Swagger UI

---

## Requisitos
- Python 3.11
- pip
- PostgreSQL 12+
- Docker (opcional pero recomendado)

---

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/parachwriter/Kamina_digital_library
cd Kamina_digital_library
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
source .venv/Scripts/Activate  # En caso que el comando de arriba no funcione

pip install -r requirements.txt
```

En caso de no responder en Windows al ejecutar en bash, emplear:
```bash
py --version
```
Si esto responde entonces usar:
```bash
py -m venv .venv
py -3.11 -m venv .venv

```

### 3. Configurar variables de entorno

Crear un archivo `.env` con el siguiente contenido:

```env
APP_NAME=Kamina Digital Library
DATABASE_URL=postgresql+asyncpg://admin:admin123@localhost:5432/kamina
SECRET_KEY=mi_secreta_clave_super_segura_123456
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Crear base de datos

Se usó PostgreSQL, para tenerlo corriendo ejecutar:
```bash
createdb kamina
```
Para levantar el contenedor, usar el siguiente comando: 
```bash

docker run -d --name kamina-postgres -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=kamina -p 5432:5432 postgres:15



```
### 5. Crear tablas de la base de datos 
```bash
python app/test/create_tables.py

```
o
```bash
python -m app.test.create_tables
python -m app.test.create_tables

```
### 6. Comprobar desde la base de datos la creacion de las tablas
```bash
docker exec -it kamina-postgres psql -U admin -d kamina
```
entonces usar
```bash
\dt

```

---

## 🏗️ Estructura del proyecto
```
Kamina/
├── app/
│   ├── main.py
│   ├── db/
│   │   ├── models/     # Entidades (User, Author, Book)
│   │   └── session.py
│   ├── routers/        # Rutas de la API
│   ├── schemas/        # Validaciones con Pydantic
│   ├── services/       # Lógica de negocio
│   ├── crud/           # Operaciones CRUD
│   └── core/
│       ├── security.py  # Autenticación y seguridad
│       └── config.py    # Variables de entorno
├── test/               # Tests unitarios con pytest
└── .env                # Configuración de variables de entorno

```

---

## Ejecutar la aplicación
```bash
uvicorn app.main:app --reload
```

En caso de que el puerto esté ocupado usar:
```bash
uvicorn app.main:app --reload --port 9000
# o cualquier otro puerto no utilizado
```

### Documentación Swagger:
```bash
http://localhost:8000/docs
```

### Pruebas

Ejecutar todas las pruebas:
```bash
coverage run -m pytest
coverage report -m
```

---

## Endpoints
- `.env` — Variables de entorno
- `requirements.txt` — Librerías necesarias
- `app/main.py` — Punto de entrada principal
- `app/test/create_tables.py` — Script para crear las tablas de la base de datos

--- 

## Notas adicionales

### Base de datos
La aplicación requiere PostgreSQL 12+. Asegúrate de tener una instancia corriendo antes de ejecutar la aplicación.

### Configuración de base de datos
Por defecto, se usa la siguiente configuración:
- Usuario: `admin`
- Contraseña: `admin123` 
- Base de datos: `kamina`
- Puerto: `5432`

Si necesitas cambiar estos valores, modifica el campo `DATABASE_URL` en tu archivo `.env`.

### Pruebas unitarias
Para ejecutar las pruebas con cobertura:
```bash
coverage run -m pytest
coverage report -m
```

Los tests cubren más del 80% del código y utilizan mocks para simular dependencias externas.

---
