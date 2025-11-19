from fastapi import APIRouter, Depends, Response, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_async_db
from app.services.book_service import book_service
from app.schemas.book import CreateBook, UpdateBook, BookOut, SearchBook, SearchBookOut

router = APIRouter(prefix="/books", tags=["books"])


# Todos los endpoints NO requieren usuario autenticado
@router.get("", response_model=List[BookOut])
async def get_books(session: AsyncSession = Depends(get_async_db)):
    return await book_service.consult_all(session)


@router.get("/search", response_model=List[SearchBookOut])
async def search_books(
    title: Optional[str] = Query(None, example="El principito"),
    author_name: Optional[str] = Query(None, example="Agatha Christie"),
    year: Optional[int] = Query(None, example=2008),
    session: AsyncSession = Depends(get_async_db)
):
    search_data = SearchBook(title=title, author_name=author_name, year=year)
    return await book_service.search(session, search_data)


@router.get("/{book_id}", response_model=BookOut)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(get_async_db)
):
    return await book_service.consult_by_id(session, book_id)


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: CreateBook,
    session: AsyncSession = Depends(get_async_db)
):
    return await book_service.register(session, book)


@router.patch("/{book_id}", response_model=BookOut)
async def update_book(
    book_id: int,
    updates: UpdateBook,
    session: AsyncSession = Depends(get_async_db)
):
    return await book_service.update(session, book_id, updates)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_async_db)
):
    await book_service.delete(session, book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{book_id}/borrow", response_model=BookOut)
async def borrow_book(
    book_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_async_db)
):
    return await book_service.borrow(session, book_id, user_id)


@router.post("/{book_id}/return", response_model=BookOut)
async def return_book(
    book_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_async_db)
):
    return await book_service.return_book(session, book_id, user_id)
