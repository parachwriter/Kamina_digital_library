from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import book_crud, author_crud
from app.db.models.book import Book
from app.schemas.book import CreateBook, UpdateBook, SearchBook, SearchBookOut
from app.services.user_service import user_service


class BookService:

    async def is_valid_author_id(self, session: AsyncSession, author_id: int) -> None:
        author = await author_crud.get_author_by_id(session, author_id)
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    async def get_by_id_with_validation(self, session: AsyncSession, book_id: int) -> Book:
        book = await book_crud.get_book_by_id(session, book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return book

    async def consult_all(self, session: AsyncSession) -> List[Book]:
        books = await book_crud.get_books(session)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found")
        return books

    async def consult_by_id(self, session: AsyncSession, book_id: int) -> Book:
        return await self.get_by_id_with_validation(session, book_id)

    async def register(self, session: AsyncSession, book_data: CreateBook) -> Book:
        await self.is_valid_author_id(session, book_data.author_id)
        new_book = Book(
            title=book_data.title,
            publication_year=book_data.publication_year,
            author_id=book_data.author_id
        )
        return await book_crud.create_book(session, new_book)

    async def update(self, session: AsyncSession, book_id: int, updates: UpdateBook) -> Book:
        book = await self.get_by_id_with_validation(session, book_id)

        if updates.title is not None:
            book.title = updates.title
        if updates.publication_year is not None:
            book.publication_year = updates.publication_year
        if updates.author_id is not None:
            await self.is_valid_author_id(session, updates.author_id)
            book.author_id = updates.author_id

        return await book_crud.update_book(session, book)

    async def delete(self, session: AsyncSession, book_id: int) -> None:
        book = await self.get_by_id_with_validation(session, book_id)
        if book.borrower_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a book that is currently borrowed"
            )
        await book_crud.delete_book(session, book)

    async def search(self, session: AsyncSession, book_search: SearchBook) -> List[SearchBookOut]:
        books_query = await book_crud.search_book(session, book_search)
        for b in books_query:
            await session.refresh(b, attribute_names=["author"])
        if not books_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")
        return [
            SearchBookOut(
                id=b.id,
                title=b.title,
                publication_year=b.publication_year,
                author_name=b.author.name if b.author else "",
                borrower_id=b.borrower_id
            )
            for b in books_query
        ]

    async def borrow(self, session: AsyncSession, book_id: int, user_id: int) -> Book:
        await user_service.get_by_id_with_validation(session, user_id)
        book = await self.get_by_id_with_validation(session, book_id)
        if book.borrower_id is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is already borrowed")
        book.borrower_id = user_id
        return await book_crud.update_book(session, book)

    async def return_book(self, session: AsyncSession, book_id: int, user_id: int) -> Book:
        await user_service.get_by_id_with_validation(session, user_id)
        book = await self.get_by_id_with_validation(session, book_id)
        if book.borrower_id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book not borrowed by this user")
        book.borrower_id = None
        return await book_crud.update_book(session, book)


book_service = BookService()
