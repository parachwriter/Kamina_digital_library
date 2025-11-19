import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import OperationalError
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger("uvicorn.error")

engine = create_async_engine(settings.DATABASE_URL,
                              echo = False
)
AsyncLocalSession = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=AsyncSession)

async def get_async_db():
    async with AsyncLocalSession() as session:
        try:
            yield session
        except OperationalError as oe:
            logger.error(f"Ocurrió un error al conectar con la base de datos: {oe}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Fallo en la base de datos"
            )
# como estoy usando async no debo cerrar "manualmente"