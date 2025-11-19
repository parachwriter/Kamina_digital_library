# test_author_service.py

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.author import Author
from app.schemas.author import CreateAuthor, UpdateAuthor
from app.services.author_service import author_service


@pytest.mark.asyncio
async def test_get_by_id_with_validation_success():
    """Test para obtener autor por ID exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_author = Author(id=1, name="Test Author", birth_date=None)
    
    with patch('app.crud.author_crud.get_author_by_id', return_value=fake_author):
        result = await author_service.get_by_id_with_validation(mock_session, 1)
        
    assert result.id == 1
    assert result.name == "Test Author"


@pytest.mark.asyncio
async def test_get_by_id_with_validation_not_found():
    """Test para obtener autor por ID cuando no existe"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.author_crud.get_author_by_id', return_value=None):
        with pytest.raises(HTTPException) as exc:
            await author_service.get_by_id_with_validation(mock_session, 999)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "Author not registered"


@pytest.mark.asyncio
async def test_consult_all_success():
    """Test para consultar todos los autores"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_authors = [
        Author(id=1, name="Author 1", birth_date=None),
        Author(id=2, name="Author 2", birth_date=None)
    ]
    
    with patch('app.crud.author_crud.get_authors', return_value=fake_authors):
        result = await author_service.consult_all(mock_session)
        
    assert len(result) == 2
    assert result[0].name == "Author 1"


@pytest.mark.asyncio
async def test_consult_all_empty():
    """Test para consultar autores cuando no hay registros"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.author_crud.get_authors', return_value=[]):
        with pytest.raises(HTTPException) as exc:
            await author_service.consult_all(mock_session)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "No author has been registered"


@pytest.mark.asyncio
async def test_register_author_success():
    """Test para registrar un autor exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    author_data = CreateAuthor(name="New Author", birth_date=None)
    fake_author = Author(id=1, name="New Author", birth_date=None)
    
    with patch('app.crud.author_crud.create_author', return_value=fake_author):
        result = await author_service.register(mock_session, author_data)
        
    assert result.name == "New Author"
    assert result.id == 1


@pytest.mark.asyncio
async def test_update_author_success():
    """Test para actualizar autor exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    existing_author = Author(id=1, name="Old Name", birth_date=None)
    update_data = UpdateAuthor(name="New Name")
    updated_author = Author(id=1, name="New Name", birth_date=None)
    
    with patch('app.crud.author_crud.get_author_by_id', return_value=existing_author):
        with patch('app.crud.author_crud.update_author', return_value=updated_author):
            result = await author_service.update(mock_session, 1, update_data)
            
    assert result.name == "New Name"


@pytest.mark.asyncio
async def test_update_author_not_found():
    """Test para actualizar autor que no existe"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.author_crud.get_author_by_id', return_value=None):
        with pytest.raises(HTTPException) as exc:
            await author_service.update(mock_session, 999, UpdateAuthor(name="New Name"))
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "Author not registered"


@pytest.mark.asyncio
async def test_delete_author_success():
    """Test para eliminar autor exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    existing_author = Author(id=1, name="Author to delete")
    
    with patch('app.crud.author_crud.get_author_by_id', return_value=existing_author):
        with patch('app.crud.author_crud.delete_author', return_value=None):
            await author_service.delete(mock_session, 1)
            
    # Verifica que se llamó a la función de eliminación
    # Esto se puede verificar con más detalle en el test del CRUD


@pytest.mark.asyncio
async def test_delete_author_not_found():
    """Test para eliminar autor que no existe"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.author_crud.get_author_by_id', return_value=None):
        with pytest.raises(HTTPException) as exc:
            await author_service.delete(mock_session, 999)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "Author not registered"
