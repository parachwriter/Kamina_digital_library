import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import user_service
from app.db.models.user import User


# ============================================================
# CREATE USER
# ============================================================
@pytest.mark.asyncio
async def test_create_user_with_mock(mocker):
    """Debe llamar a user_crud.create_user después de validar email."""
    mock_session = AsyncMock(spec=AsyncSession)

    mocker.patch("app.crud.user_crud.get_user_by_email", return_value=None)
    mocker.patch("app.core.security.encrypt_password", return_value="encrypted")

    mock_create = mocker.patch(
        "app.crud.user_crud.create_user",
        return_value=User(id=1, name="John", email="john@example.com", password_hash="encrypted")
    )

    result = await user_service.create_user(
        session=mock_session,
        name="John",
        email="john@example.com",
        password="password123"
    )

    mock_create.assert_called_once()
    assert result.id == 1
    assert result.email == "john@example.com"


@pytest.mark.asyncio
async def test_create_user_duplicate_email(mocker):
    """Debe lanzar HTTP 409 si el email ya existe."""
    mock_session = AsyncMock()

    mocker.patch(
        "app.crud.user_crud.get_user_by_email",
        return_value=User(id=2, name="Existing", email="john@example.com", password_hash="x")
    )

    with pytest.raises(HTTPException) as exc:
        await user_service.create_user(
            session=mock_session,
            name="John",
            email="john@example.com",
            password="StrongPassword123"
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Email already in use"


# ============================================================
# UPDATE USER
# ============================================================
@pytest.mark.asyncio
async def test_update_user_success(mocker):
    """Debe actualizar correctamente el nombre del usuario."""
    mock_session = AsyncMock()

    fake_user = User(id=1, name="Old Name", email="old@example.com", password_hash="hash")

    mocker.patch.object(user_service, "get_by_id_with_validation", return_value=fake_user)
    mocker.patch("app.crud.user_crud.get_user_by_email", return_value=None)
    mock_update = mocker.patch("app.crud.user_crud.update_user", return_value=fake_user)

    result = await user_service.update_user(
        session=mock_session,
        user_id=1,
        name="New Name"
    )

    mock_update.assert_called_once()
    assert result.name == "New Name"


@pytest.mark.asyncio
async def test_update_user_duplicate_email(mocker):
    """Debe lanzar HTTP 400 si el email ya está registrado por otro usuario."""
    mock_session = AsyncMock()

    fake_user = User(id=1, name="John", email="john@example.com", password_hash="x")

    mocker.patch.object(user_service, "get_by_id_with_validation", return_value=fake_user)
    mocker.patch(
        "app.crud.user_crud.get_user_by_email",
        return_value=User(id=2, name="Other", email="exists@example.com", password_hash="y")
    )

    with pytest.raises(HTTPException) as exc:
        await user_service.update_user(
            session=mock_session,
            user_id=1,
            email="exists@example.com"
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already registered"


@pytest.mark.asyncio
async def test_update_user_password(mocker):
    """Debe actualizar correctamente la contraseña."""
    mock_session = AsyncMock()

    fake_user = User(id=1, name="John", email="john@example.com", password_hash="oldhash")

    mocker.patch.object(user_service, "get_by_id_with_validation", return_value=fake_user)
    mocker.patch("app.crud.user_crud.get_user_by_email", return_value=None)
    mock_encrypt = mocker.patch("app.core.security.encrypt_password", return_value="new_hash")
    mock_update = mocker.patch("app.crud.user_crud.update_user", return_value=fake_user)

    result = await user_service.update_user(
        session=mock_session,
        user_id=1,
        password="NewPass123"
    )

    mock_encrypt.assert_called_once()
    mock_update.assert_called_once()
    assert result.password_hash == "new_hash"


# ============================================================
# AUTHENTICATION
# ============================================================
@pytest.mark.asyncio
async def test_authenticate_success(mocker):
    """Debe autenticar correctamente si email y password coinciden."""
    mock_session = AsyncMock()

    fake_user = User(id=1, name="John", email="john@example.com", password_hash="hashed")

    mocker.patch("app.crud.user_crud.get_user_by_email", return_value=fake_user)
    mocker.patch("app.core.security.validate_password", return_value=True)

    user = await user_service.authenticate(
        session=mock_session,
        email="john@example.com",
        password="correctpassword"
    )

    assert user.id == 1
    assert user.email == "john@example.com"


@pytest.mark.asyncio
async def test_authenticate_wrong_password(mocker):
    """Debe lanzar 401 si la contraseña es incorrecta."""
    mock_session = AsyncMock()

    fake_user = User(id=1, name="John", email="john@example.com", password_hash="hashed")

    mocker.patch("app.crud.user_crud.get_user_by_email", return_value=fake_user)
    mocker.patch("app.core.security.validate_password", return_value=False)

    with pytest.raises(HTTPException) as exc:
        await user_service.authenticate(
            session=mock_session,
            email="john@example.com",
            password="wrongpassword"
        )

    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect email or password"


# ============================================================
# GET USERS
# ============================================================
@pytest.mark.asyncio
async def test_get_all_users_success(mocker):
    mock_session = AsyncMock()

    fake_users = [
        User(id=1, name="A", email="a@example.com", password_hash="x"),
        User(id=2, name="B", email="b@example.com", password_hash="y")
    ]

    mocker.patch("app.crud.user_crud.get_users", return_value=fake_users)

    users = await user_service.get_all_users(session=mock_session)

    assert len(users) == 2
    assert users[0].name == "A"


@pytest.mark.asyncio
async def test_get_all_users_empty(mocker):
    mock_session = AsyncMock()

    mocker.patch("app.crud.user_crud.get_users", return_value=[])

    with pytest.raises(HTTPException) as exc:
        await user_service.get_all_users(session=mock_session)

    assert exc.value.status_code == 404
    assert exc.value.detail == "No users registered"


# ============================================================
# DELETE USER
# ============================================================
@pytest.mark.asyncio
async def test_delete_user_success(mocker):
    """Debe eliminar el usuario si existe."""
    mock_session = AsyncMock()

    fake_user = User(id=1, name="John", email="john@example.com", password_hash="x")

    mocker.patch.object(user_service, "get_by_id_with_validation", return_value=fake_user)
    mock_delete = mocker.patch("app.crud.user_crud.delete_user", return_value=None)

    result = await user_service.delete_user(session=mock_session, user_id=1)

    mock_delete.assert_called_once_with(mock_session, fake_user)
    assert result is None


@pytest.mark.asyncio
async def test_delete_user_not_found(mocker):
    """Debe lanzar 404 si el usuario no existe."""
    mock_session = AsyncMock()

    mocker.patch.object(
        user_service,
        "get_by_id_with_validation",
        side_effect=HTTPException(status_code=404, detail="User not found")
    )

    with pytest.raises(HTTPException) as exc:
        await user_service.delete_user(session=mock_session, user_id=999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
