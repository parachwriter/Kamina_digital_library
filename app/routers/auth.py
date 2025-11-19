from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db
from app.db.models.user import User
from app.schemas.user import UserOut
from app.services import auth as auth_service
from app.schemas.auth import JWT
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


# Login usando solo email y password
@router.post("/login", response_model=JWT)
async def login(
    email: str = Form(..., example="user@example.com"),
    password: str = Form(..., example="StrongPass123"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Endpoint de login que devuelve un JWT.
    Swagger UI solo pedirá email y password.
    """
    return await auth_service.login(db, email, password)


# Endpoint para obtener el usuario actual
@router.get("/me", response_model=UserOut)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """
    Devuelve los datos del usuario autenticado según el JWT enviado en headers.
    """
    return current_user
