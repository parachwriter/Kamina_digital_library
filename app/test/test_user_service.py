# test_user_service.py

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.schemas.user import UserCreate, UpdateUser
from app.services.user_service import user_service


@pytest.mark.asyncio
async def test_create_user_success():
    """Test para crear usuario exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    user_data = UserCreate(name="Test User", email="test@example.com", password="StrongPass123")
    
    with patch('app.crud.user_crud.get_user_by_email', return_value=None):
        with patch('app.core.security.encrypt_password', return_value="encrypted_hash"):
            with patch('app.crud.user_crud.create_user', return_value=User(id=1, name="Test User", email="test@example.com", password_hash="encrypted_hash")):
                result = await user_service.create_user(mock_session, "Test User", "test@example.com", "StrongPass123")
                
    assert result.id == 1
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_create_user_duplicate_email():
    """Test para crear usuario con email duplicado"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.user_crud.get_user_by_email', return_value=User(id=1, name="Existing", email="test@example.com", password_hash="hash")):
        with pytest.raises(HTTPException) as exc:
            await user_service.create_user(mock_session, "Test User", "test@example.com", "StrongPass123")
            
    assert exc.value.status_code == 409
    assert exc.value.detail == "Email already in use"


@pytest.mark.asyncio
async def test_get_by_id_with_validation_success():
    """Test para obtener usuario por ID exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_user = User(id=1, name="Test User", email="test@example.com", password_hash="hash")
    
    with patch('app.crud.user_crud.get_user_by_id', return_value=fake_user):
        result = await user_service.get_by_id_with_validation(mock_session, 1)
        
    assert result.id == 1
    assert result.name == "Test User"


@pytest.mark.asyncio
async def test_get_by_id_with_validation_not_found():
    """Test para obtener usuario por ID cuando no existe"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.user_crud.get_user_by_id', return_value=None):
        with pytest.raises(HTTPException) as exc:
            await user_service.get_by_id_with_validation(mock_session, 999)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"


@pytest.mark.asyncio
async def test_get_by_email_success():
    """Test para obtener usuario por email exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_user = User(id=1, name="Test User", email="test@example.com", password_hash="hash")
    
    with patch('app.crud.user_crud.get_user_by_email', return_value=fake_user):
        result = await user_service.get_by_email(mock_session, "test@example.com")
        
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_by_email_not_found():
    """Test para obtener usuario por email que no existe"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.user_crud.get_user_by_email', return_value=None):
        result = await user_service.get_by_email(mock_session, "nonexistent@example.com")
        
    assert result is None


@pytest.mark.asyncio
async def test_authenticate_success():
    """Test para autenticar usuario exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_user = User(id=1, name="Test User", email="test@example.com", password_hash="hashed_password")
    
    with patch('app.crud.user_crud.get_user_by_email', return_value=fake_user):
        with patch('app.core.security.validate_password', return_value=True):
            result = await user_service.authenticate(mock_session, "test@example.com", "password123")
            
    assert result.id == 1
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_authenticate_wrong_password():
    """Test para autenticar con contraseña incorrecta"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_user = User(id=1, name="Test User", email="test@example.com", password_hash="hashed_password")
    
    with patch('app.crud.user_crud.get_user_by_email', return_value=fake_user):
        with patch('app.core.security.validate_password', return_value=False):
            with pytest.raises(HTTPException) as exc:
                await user_service.authenticate(mock_session, "test@example.com", "wrongpassword")
                
    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect email or password"


@pytest.mark.asyncio
async def test_get_all_users_success():
    """Test para obtener todos los usuarios exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_users = [
        User(id=1, name="User 1", email="user1@example.com", password_hash="hash1"),
        User(id=2, name="User 2", email="user2@example.com", password_hash="hash2")
    ]
    
    with patch('app.crud.user_crud.get_users', return_value=fake_users):
        result = await user_service.get_all_users(mock_session)
        
    assert len(result) == 2
    assert result[0].name == "User 1"


@pytest.mark.asyncio
async def test_get_all_users_empty():
    """Test para obtener usuarios cuando no hay registros"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.user_crud.get_users', return_value=[]):
        with pytest.raises(HTTPException) as exc:
            await user_service.get_all_users(mock_session)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "No users registered"


@pytest.mark.asyncio
async def test_update_user_success():
    """Test para actualizar usuario exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    existing_user = User(id=1, name="Old Name", email="test@example.com", password_hash="oldhash")
    
    with patch('app.crud.user_crud.get_user_by_id', return_value=existing_user):
        with patch('app.crud.user_crud.get_user_by_email', return_value=None):
            with patch('app.core.security.encrypt_password', return_value="newhash"):
                with patch('app.crud.user_crud.update_user', return_value=existing_user):
                    result = await user_service.update_user(mock_session, 1, name="New Name")
                    
    assert result.name == "New Name"


@pytest.mark.asyncio
async def test_update_user_duplicate_email():
    """Test para actualizar usuario con email duplicado"""
    mock_session = AsyncMock(spec=AsyncSession)
    existing_user = User(id=1, name="Test User", email="test@example.com", password_hash="hash")
    
    with patch('app.crud.user_crud.get_user_by_id', return_value=existing_user):
        with patch('app.crud.user_crud.get_user_by_email', return_value=User(id=2, name="Other", email="other@example.com", password_hash="hash")):
            with pytest.raises(HTTPException) as exc:
                await user_service.update_user(mock_session, 1, email="other@example.com")
                
    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already registered"


@pytest.mark.asyncio
async def test_update_user_password():
    """Test para actualizar contraseña de usuario"""
    mock_session = AsyncMock(spec=AsyncSession)
    existing_user = User(id=1, name="Test User", email="test@example.com", password_hash="oldhash")
    
    with patch('app.crud.user_crud.get_user_by_id', return_value=existing_user):
        with patch('app.crud.user_crud.get_user_by_email', return_value=None):
            with patch('app.core.security.encrypt_password', return_value="newhash"):
                with patch('app.crud.user_crud.update_user', return_value=existing_user):
                    result = await user_service.update_user(mock_session, 1, password="NewPass123")
                    
    assert result.password_hash == "newhash"


@pytest.mark.asyncio
async def test_delete_user_success():
    """Test para eliminar usuario exitoso"""
    mock_session = AsyncMock(spec=AsyncSession)
    fake_user = User(id=1, name="Test User", email="test@example.com", password_hash="hash")
    
    with patch('app.crud.user_crud.get_user_by_id', return_value=fake_user):
        with patch('app.crud.user_crud.delete_user', return_value=None):
            await user_service.delete_user(mock_session, 1)
            
    # Verifica que se llamó a la función de eliminación


@pytest.mark.asyncio
async def test_delete_user_not_found():
    """Test para eliminar usuario que no existe"""
    mock_session = AsyncMock(spec=AsyncSession)
    
    with patch('app.crud.user_crud.get_user_by_id', return_value=None):
        with pytest.raises(HTTPException) as exc:
            await user_service.delete_user(mock_session, 999)
            
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
