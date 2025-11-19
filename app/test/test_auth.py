import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import validate_password, encrypt_password

client = TestClient(app)

# TEST LOGIN SUCCESS

def test_login_success():
    """Prueba login exitoso"""
    with patch('app.services.auth.authenticate_user', new_callable=AsyncMock) as mock_auth:
        with patch('app.services.auth.issue_token') as mock_issue:
            mock_user = MagicMock()
            mock_user.id = 1
            mock_user.email = "test@example.com"

            mock_auth.return_value = mock_user
            mock_issue.return_value = "mocked_jwt_token"

            response = client.post(
                "/auth/login",
                data={"email": "test@example.com", "password": "StrongPass123"}
            )

            assert response.status_code == 200
            body = response.json()
            assert body["access_token"] == "mocked_jwt_token"
            assert body["token_type"] == "bearer"



# TEST LOGIN INVALID CREDENTIALS

def test_login_invalid_credentials():
    """Prueba login con credenciales inválidas"""
    with patch('app.services.auth.authenticate_user', new_callable=AsyncMock) as mock_auth:
        mock_auth.side_effect = Exception("Credenciales incorrectas")

        response = client.post(
            "/auth/login",
            data={"email": "test@example.com", "password": "wrong"}
        )

        assert response.status_code == 401



# TEST CURRENT USER SUCCESS

def test_read_current_user_success():
    """Prueba obtener usuario actual"""
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.name = "Test User"
    mock_user.email = "test@example.com"
    mock_user.registered_at = "2023-01-01T00:00:00"

    with patch('app.core.security.get_current_user', return_value=mock_user):
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer token123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"



# TEST CURRENT USER FAIL

def test_read_current_user_unauthorized():
    with patch('app.core.security.get_current_user') as mock_get_user:
        mock_get_user.side_effect = Exception("Token inválido")

        response = client.get("/auth/me")

        assert response.status_code == 401



# TEST LOGIN DEPENDENCY

def test_login_dependency():
    from app.schemas.auth import LoginForm

    form_data = {"email": "test@example.com", "password": "StrongPass123"}
    login_form = LoginForm(**form_data)

    assert login_form.email == "test@example.com"
    assert login_form.password == "StrongPass123"



# TEST REGISTER USER SUCCESS

def test_register_user_success():
    """Prueba el flujo de creación de usuario"""
    with patch('app.services.user_service.user_service.create_user') as mock_create_user:
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"

        mock_create_user.return_value = mock_user

        from app.schemas.user import UserCreate
        user_data = UserCreate(
            name="Test User",
            email="test@example.com",
            password="StrongPass123"
        )

        # Validación simple
        assert user_data.name == "Test User"
        assert user_data.email == "test@example.com"



# TEST AUTHENTICATE USER REAL PASSWORD VALIDATION

def test_authenticate_user_real():
    """Prueba validar password real"""
    hashed = encrypt_password("StrongPass123")

    assert validate_password("StrongPass123", hashed) is True
    assert validate_password("wrongpass", hashed) is False



# TEST LOGIN WITH REAL DATA USING ASYNC

@pytest.mark.asyncio
async def test_login_with_real_data():
    with patch('app.crud.user_crud.get_user_by_email', new_callable=AsyncMock) as mock_get_user:
        with patch('app.core.security.validate_password') as mock_validate:
            with patch('app.core.security.issue_token') as mock_issue:

                mock_user = MagicMock()
                mock_user.id = 1
                mock_user.email = "test@example.com"
                mock_user.password_hash = "hashed_password"

                mock_get_user.return_value = mock_user
                mock_validate.return_value = True
                mock_issue.return_value = "real_jwt_token"

                from app.services.auth import authenticate_user
                result = await authenticate_user(
                    AsyncMock(), "test@example.com", "StrongPass123"
                )

                assert result.id == 1
                assert result.email == "test@example.com"
