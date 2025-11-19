import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException

from app.services.book_service import book_service
from app.schemas.book import CreateBook
from app.db.models.book import Book



# TEST 1: REGISTRO DE LIBRO (CAMINO FELIZ)

@pytest.mark.asyncio
async def test_register_book_success(mocker):
    """
    Verifica que book_service.register:
    - valida el autor
    - llama a create_book
    - devuelve el libro creado
    """

    session = AsyncMock()

    # Mock: el autor sí existe
    mock_author_check = mocker.patch.object(
        book_service,
        "is_valid_author_id",
        new_callable=AsyncMock
    )

    # Fake book retornado por la capa CRUD
    fake_book = Book(
        id=1,
        title="Test Book",
        publication_year=2024,
        author_id=1,
        borrower_id=None
    )

    mock_create = mocker.patch(
        "app.crud.book_crud.create_book",
        return_value=fake_book
    )

    # Ejecutar
    payload = CreateBook(
        title="Test Book",
        author_id=1,
        publication_year=2024
    )
    result = await book_service.register(session, payload)

    # Asserts
    mock_author_check.assert_awaited_once_with(session, 1)
    mock_create.assert_called_once()
    assert result == fake_book
    assert result.author_id == 1
    assert result.title == "Test Book"



# TEST 2: ERROR CUANDO EL AUTOR NO EXISTE

@pytest.mark.asyncio
async def test_register_book_invalid_author(mocker):
    """
    book_service.register debe lanzar 404 si el autor no existe.
    """

    session = AsyncMock()

    # Forzar que is_valid_author_id lance la excepción
    mocker.patch.object(
        book_service,
        "is_valid_author_id",
        side_effect=HTTPException(status_code=404, detail="Author not found")
    )

    payload = CreateBook(
        title="Libro",
        author_id=99,  # autor inexistente
        publication_year=2024
    )

    with pytest.raises(HTTPException) as exc:
        await book_service.register(session, payload)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Author not found"
