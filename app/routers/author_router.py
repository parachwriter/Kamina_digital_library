from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_async_db
from app.services.author_service import author_service
from app.schemas.author import CreateAuthor, UpdateAuthor, AuthorOut

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("", response_model=List[AuthorOut])
async def get_authors(session: AsyncSession = Depends(get_async_db)):
    return await author_service.consult_all(session)


@router.get("/{author_id}", response_model=AuthorOut)
async def get_author(author_id: int, session: AsyncSession = Depends(get_async_db)):
    return await author_service.consult_by_id(session, author_id)


@router.post("", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
async def create_author(author: CreateAuthor, session: AsyncSession = Depends(get_async_db)):
    return await author_service.register(session, author)


@router.patch("/{author_id}", response_model=AuthorOut)
async def update_author(author_id: int, updates: UpdateAuthor, session: AsyncSession = Depends(get_async_db)):
    return await author_service.update(session, author_id, updates)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int, session: AsyncSession = Depends(get_async_db)):
    await author_service.delete(session, author_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
