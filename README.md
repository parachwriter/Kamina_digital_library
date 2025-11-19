# Kamina Digital Library
API REST para gestión de biblioteca digital con FastAPI


##Funciones del proyecto 
- Suite de Pruebas Unitarias utilizando **pytest**, incluyendo **mocks**
- Gestión completa (CRUD) de **Usuarios, Autores y Libros**

- Función de **búsqueda** de libros por título, autor o fecha de publicación

- Control de **préstamos** y retornos de ejemplares

- Sistema de autenticación basado en JWT

- Generación automática de documentación con Swagger UI

---

##  Requisitos
- Python 3.11+
- pip
- PostgreSQL 12+
- Docker (opcional pero recomendado)

---

##  Instalación

### 1. Clonar el repositorio
```sh
git clone https://github.com/parachwriter/Kamina_digital_library
cd Kamina_digital_library
```
---
### 2. Crear entorno virtual
```env
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---
### 3. Configurar variables de entorno

Crear un archivo .env con:

APP_NAME=Kamina Digital Library
DATABASE_URL=postgresql+asyncpg://admin:admin123@localhost:5432/kamina
SECRET_KEY=mi_secreta_clave_super_segura_123456
ACCESS_TOKEN_EXPIRE_MINUTES=30

---

### 4. Crear base de datos

Se usó PostgreSQL, para tenerlo corriendo ejecutar:
createdb kamina

---
### 5. crear tablas de la base de datos 
python app/test/create_tables.py



---

```
### 🏗️ Estructura del proyecto
Kamina/
├── app/
│ ├── main.py
│ ├── db/
│ │ ├── models/
│ │ ├── session.py
│ │ └── base.py
│ ├── schemas/
│ ├── services/
│ └── routers/
├── test/
└── .env
```
---
## Ejecutar la aplicación
uvicorn app.main:app --reload


uvicorn app.main:app --reload
en caso de que el puerto esté ocupado usar 
uvicorn app.main:app --reload --port 9000
o otro valor de un puerto no utilizado 



---
### Documentación Swagger:
```bash
http://localhost:8000/docs
```


### Pruebas

Ejecutar todas las pruebas:
```
coverage run -m pytest
coverage report -m
```


---


### Endpoints
- `.env` — Environment variables
- `requirements.txt` — Librerias necesarias
- `app/main.py` — Main
- `app/tests/create_tables.py` — Crear las tablas de la base de datos

