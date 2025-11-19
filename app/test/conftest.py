# app/test/conftest.py
import asyncio
import os
import tempfile
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import OperationalError
from app.main import app
from app.db.base import Base
from app.db.session import get_async_db as real_get_async_db

# --- Usar un archivo sqlite temporal para pruebas (evita problemas de memoria compartida) ---
_tmp_file = tempfile.NamedTemporaryFile(prefix="kamina_test_", suffix=".db", delete=False)
DATABASE_FILE = _tmp_file.name
_tmp_file.close()
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE}"

# Engine y sessionmaker para tests
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


import app.db.models.author  # noqa: F401
import app.db.models.book   # noqa: F401
import app.db.models.user   # noqa: F401

@pytest.fixture(scope="function")
async def session():
    # create_all
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    # drop_all
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # borrar archivo sqlite para dejar el entorno limpio
    try:
        os.remove(DATABASE_FILE)
    except FileNotFoundError:
        pass


@pytest.fixture(scope="function")
async def client(session: AsyncSession):

    async def override_get_db():
        try:
            yield session
        except OperationalError:
            # Si algo falla en la conexión dentro de las pruebas, levantamos para que el test lo capture.
            raise

    # override la dependencia real por la de testing
    app.dependency_overrides[real_get_async_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    # limpiar override para evitar efectos colaterales entre tests
    app.dependency_overrides.pop(real_get_async_db, None)
