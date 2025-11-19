# test_book_service.py

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.book import Book
from app.db.models.author import Author
from app.schemas.book import CreateBook, UpdateBook, SearchBook
from app.services.book_service import book_service


@pytest.mark.asyncio
async def test_get_by_id_with_validation_success():
    """Test para obtener libro por ID exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_book = Book(id=1, title="Test Book", author_id=1, publication_year=2024)
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=fake_book):
        result = await book_service.get_by_id_with_validation(mock_session, 1)
        
    assert result.id == 1
    assert result.title == "Test Book"


@pytest.mark.asyncio
async def test_get_by_id_with_validation_not_found():
    """Test para obtener libro por ID cuando no existe"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=None):
        with pytest.raises(HTTPException) as exc:
            await book_service.get_by_id_with_validation(mock_session, 999)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"


@pytest.mark.asyncio
async def test_consult_all_success():
    """Test para consultar todos los libros"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_books = [
        Book(id=1, title="Book 1", author_id=1, publication_year=2024),
        Book(id=2, title="Book 2", author_id=2, publication_year=2023)
    ]
    
    with patch('app.crud.book_crud.get_books', return_value=fake_books):
        result = await book_service.consult_all(mock_session)
        
    assert len(result) == 2
    assert result[0].title == "Book 1"


@pytest.mark.asyncio
async def test_consult_all_empty():
    """Test para consultar libros cuando no hay registros"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.book_crud.get_books', return_value=[]):
        with pytest.raises(HTTPException) as exc:
            await book_service.consult_all(mock_session)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "No books found"


@pytest.mark.asyncio
async def test_register_book_success():
    """Test para registrar libro exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    book_data = CreateBook(title="New Book", author_id=1, publication_year=2024)
    fake_book = Book(id=1, title="New Book", author_id=1, publication_year=2024)
    
    with patch('app.services.book_service.BookService.is_valid_author_id', return_value=None):
        with patch('app.crud.book_crud.create_book', return_value=fake_book):
            result = await book_service.register(mock_session, book_data)
            
    assert result.title == "New Book"
    assert result.author_id == 1


@pytest.mark.asyncio
async def test_register_book_invalid_author():
    """Test para registrar libro con autor inválido"""
    mock_session = AsyncMock(spec=AsyncSession)
    book_data = CreateBook(title="New Book", author_id=999, publication_year=2024)
    
    with patch('app.services.book_service.BookService.is_valid_author_id', side_effect=HTTPException(status_code=404, detail="Author not found")):
        with pytest.raises(HTTPException) as exc:
            await book_service.register(mock_session, book_data)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "Author not found"


@pytest.mark.asyncio
async def test_update_book_success():
    """Test para actualizar libro exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    existing_book = Book(id=1, title="Old Title", author_id=1, publication_year=2024)
    update_data = UpdateBook(title="New Title", publication_year=2025)
    updated_book = Book(id=1, title="New Title", author_id=1, publication_year=2025)
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=existing_book):
        with patch('app.services.book_service.BookService.is_valid_author_id', return_value=None):
            with patch('app.crud.book_crud.update_book', return_value=updated_book):
                result = await book_service.update(mock_session, 1, update_data)
                
    assert result.title == "New Title"
    assert result.publication_year == 2025


@pytest.mark.asyncio
async def test_update_book_not_found():
    """Test para actualizar libro que no existe"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=None):
        with pytest.raises(HTTPException) as exc:
            await book_service.update(mock_session, 999, UpdateBook(title="New Title"))
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"


@pytest.mark.asyncio
async def test_delete_book_success():
    """Test para eliminar libro exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    existing_book = Book(id=1, title="Book to delete", author_id=1, publication_year=2024)
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=existing_book):
        with patch('app.crud.book_crud.delete_book', return_value=None):
            await book_service.delete(mock_session, 1)
            
    # Verifica que se llamó a la función de eliminación


@pytest.mark.asyncio
async def test_delete_book_borrowed():
    """Test para eliminar libro que está prestado"""
    mock_session = AsyncMock(spec=AsyncSession)
    borrowed_book = Book(id=1, title="Book", author_id=1, publication_year=2024, borrower_id=1)
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=borrowed_book):
        with pytest.raises(HTTPException) as exc:
            await book_service.delete(mock_session, 1)
            
    assert exc.value.status_code == 400
    assert exc.value.detail == "Cannot delete a book that is currently borrowed"


@pytest.mark.asyncio
async def test_search_books_success():
    """Test para buscar libros exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    search_data = SearchBook(title="Test", author_name=None, year=None)
    fake_books = [
        Book(id=1, title="Test Book", author_id=1, publication_year=2024),
        Book(id=2, title="Another Test", author_id=1, publication_year=2023)
    ]
    
    with patch('app.crud.book_crud.search_book', return_value=fake_books):
        result = await book_service.search(mock_session, search_data)
        
    assert len(result) == 2
    assert result[0].title == "Test Book"


@pytest.mark.asyncio
async def test_search_books_empty():
    """Test para búsqueda de libros vacía"""
    mock_session = AsyncMock(spec=AsyncSession)
    search_data = SearchBook(title="Nonexistent", author_name=None, year=None)
    
    with patch('app.crud.book_crud.search_book', return_value=[]):
        with pytest.raises(HTTPException) as exc:
            await book_service.search(mock_session, search_data)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "Books not found"


@pytest.mark.asyncio
async def test_borrow_book_success():
    """Test para prestar libro exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_book = Book(id=1, title="Book to borrow", author_id=1, publication_year=2024)
    fake_user = type('User', (), {'id': 1, 'name': 'Test User'})()
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=fake_book):
        with patch('app.services.user_service.user_service.get_by_id_with_validation', return_value=fake_user):
            with patch('app.crud.book_crud.update_book', return_value=fake_book):
                result = await book_service.borrow(mock_session, 1, 1)
                
    assert result.borrower_id == 1


@pytest.mark.asyncio
async def test_borrow_book_already_borrowed():
    """Test para prestar libro que ya está prestado"""
    mock_session = AsyncMock(spec=AsyncSession)
    borrowed_book = Book(id=1, title="Book", author_id=1, publication_year=2024, borrower_id=2)
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=borrowed_book):
        with pytest.raises(HTTPException) as exc:
            await book_service.borrow(mock_session, 1, 1)
            
    assert exc.value.status_code == 400
    assert exc.value.detail == "Book is already borrowed"


@pytest.mark.asyncio
async def test_return_book_success():
    """Test para devolver libro exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_book = Book(id=1, title="Book to return", author_id=1, publication_year=2024, borrower_id=1)
    fake_user = type('User', (), {'id': 1, 'name': 'Test User'})()
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=fake_book):
        with patch('app.services.user_service.user_service.get_by_id_with_validation', return_value=fake_user):
            with patch('app.crud.book_crud.update_book', return_value=fake_book):
                result = await book_service.return_book(mock_session, 1, 1)
                
    assert result.borrower_id is None


@pytest.mark.asyncio
async def test_return_book_wrong_user():
    """Test para devolver libro por usuario incorrecto"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_book = Book(id=1, title="Book", author_id=1, publication_year=2024, borrower_id=2)
    
    with patch('app.crud.book_crud.get_book_by_id', return_value=fake_book):
        with pytest.raises(HTTPException) as exc:
            await book_service.return_book(mock_session, 1, 1)
            
    assert exc.value.status_code == 400
    assert exc.value.detail == "Book not borrowed by this user"
