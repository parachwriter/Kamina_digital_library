from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from typing import List

from app.db.session import get_async_db
from app.services.user_service import user_service
from app.schemas.user import UserCreate, UserOut, UpdateUser

router = APIRouter(prefix="/users", tags=["users"])



# Obtener todos los usuarios
@router.get("", response_model=List[UserOut])
async def get_users(session: AsyncSession = Depends(get_async_db)):
    return await user_service.get_all_users(session)


# Obtener usuario por email
@router.get("/by_email", response_model=UserOut)
async def get_user_by_email(
    email: EmailStr,
    session: AsyncSession = Depends(get_async_db),
):
    return await user_service.get_by_email(session, email)


# Obtener usuario por ID
@router.get("/{id}", response_model=UserOut)
async def get_user(id: int, session: AsyncSession = Depends(get_async_db)):
    return await user_service.get_by_id_with_validation(session, id)


# Crear usuario
@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_db),
):
    return await user_service.create_user(
        session,
        name=user.name,
        email=user.email,
        password=user.password
    )


# Actualizar usuario (PATCH)
@router.patch("/{id}", response_model=UserOut)
async def update_user(
    id: int,
    updates: UpdateUser,
    session: AsyncSession = Depends(get_async_db),
):
    return await user_service.update_user(
        session,
        user_id=id,
        name=updates.name,
        email=updates.email,
        password=updates.password
    )


# Eliminar usuario
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int,
    session: AsyncSession = Depends(get_async_db),
):
    await user_service.delete_user(session, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

