from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.db.models.author import Author


# Obtener todos los autores
async def get_authors(db: AsyncSession) -> List[Author]:
    result = await db.execute(select(Author))
    return result.scalars().all()   #type: ignore


# Obtener autor por ID
async def get_author_by_id(db: AsyncSession, author_id: int) -> Optional[Author]:
    result = await db.execute(select(Author).where(Author.id == author_id))
    return result.scalar_one_or_none()


# Crear autor
async def create_author(db: AsyncSession, author: Author) -> Author:
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


# Actualizar autor
async def update_author(db: AsyncSession, author: Author) -> Author:
    await db.commit()
    await db.refresh(author)
    return author


# Eliminar autor
async def delete_author(db: AsyncSession, author: Author) -> None:
    await db.delete(author)
    await db.commit()
