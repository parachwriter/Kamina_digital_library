import asyncio
from app.db.base import Base
from app.db.session import engine

async def init_models():
    async with engine.begin() as conn:
        # Esto crea todas las tablas declaradas en Base
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas correctamente")

asyncio.run(init_models())
