from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.author import Author
from app.schemas.author import CreateAuthor, UpdateAuthor
from app.crud import author_crud

class AuthorService:

    # Obtener autor por ID con validación
    async def get_by_id_with_validation(self, session: AsyncSession, author_id: int) -> Author:
        author = await author_crud.get_author_by_id(session, author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not registered"
            )
        return author

    # Consultar todos los autores
    async def consult_all(self, session: AsyncSession) -> List[Author]:
        authors = await author_crud.get_authors(session)
        if not authors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No author has been registered"
            )
        return authors

    # Consultar autor por ID
    async def consult_by_id(self, session: AsyncSession, author_id: int) -> Author:
        return await self.get_by_id_with_validation(session, author_id)

    # Registrar nuevo autor
    async def register(self, session: AsyncSession, author_data: CreateAuthor) -> Author:
        new_author = Author(
            name=author_data.name,
            birth_date=author_data.birth_date  
        )
        return await author_crud.create_author(session, new_author)

    # Actualizar autor
    async def update(self, session: AsyncSession, author_id: int, updates: UpdateAuthor) -> Author:
        author = await self.get_by_id_with_validation(session, author_id)
        if updates.name is not None:
            author.name = updates.name
        if updates.birth_date is not None:
            author.birth_date = updates.birth_date 
        return await author_crud.update_author(session, author)

    # Eliminar autor
    async def delete(self, session: AsyncSession, author_id: int) -> None:
        author = await self.get_by_id_with_validation(session, author_id)
        await author_crud.delete_author(session, author)

# Instancia global
author_service = AuthorService()
