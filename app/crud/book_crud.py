from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.db.models.book import Book
from app.db.models.author import Author
from app.schemas.book import SearchBook
from sqlalchemy.orm import selectinload

# Obtener todos
async def get_books(db: AsyncSession) -> List[Book]:
    result = await db.execute(select(Book))
    return result.scalars().all()   #type: ignore
# Obtener por ID
async def get_book_by_id(db: AsyncSession, book_id: int) -> Optional[Book]:
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()
# Crear 
async def create_book(db: AsyncSession, book: Book) -> Book:
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book
# Actualizar 
async def update_book(db: AsyncSession, book: Book) -> Book:
    await db.commit()
    await db.refresh(book)
    return book

# Eliminar 
async def delete_book(db: AsyncSession, book: Book) -> None:
    await db.delete(book)
    await db.commit()
# Buscar por filtros
async def search_book(db: AsyncSession, book_search: SearchBook) -> List[Book]:
    # Selecciona instancias de Book y carga la relación author
    stmt = select(Book).options(selectinload(Book.author))

    # Filtrado por título
    if book_search.title:
        stmt = stmt.where(Book.title.ilike(f"%{book_search.title}%"))

    # Filtrado por autor
    if book_search.author_name:
        stmt = stmt.join(Book.author).where(Author.name.ilike(f"%{book_search.author_name}%"))

    # Filtrado por año de publicación
    if book_search.year:
        stmt = stmt.where(Book.publication_year == book_search.year)

    # Ejecuta la consulta
    result = await db.execute(stmt)
    return result.scalars().all()  # Devuelve lista de Book
