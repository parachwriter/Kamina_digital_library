import asyncio
from app.db.base import Base
from app.db.session import engine
from app.db.models import user, author, book

async def init_models():
    async with engine.begin() as conn:
        # Esto crea todas las tablas declaradas en Base
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas correctamente")

    
if __name__ == "__main__":
    asyncio.run(init_models())
