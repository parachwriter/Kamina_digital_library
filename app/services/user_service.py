from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.crud import user_crud
from app.db.models.user import User
from app.core.security import encrypt_password, validate_password
from sqlalchemy import select
from typing import Optional


class UserService:

    # Crear usuario
    async def create_user(self, session: AsyncSession, name: str, email: str, password: str) -> User:
        existing_user = await user_crud.get_user_by_email(session, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use"
            )

        user = User(
            name=name,
            email=email,
            password_hash=encrypt_password(password)
        )

        return await user_crud.create_user(session, user)

    # Obtener usuario por ID con validación
    async def get_by_id_with_validation(self, session: AsyncSession, user_id: int) -> User:
        user = await user_crud.get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    # Obtener usuario por email
    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        return await user_crud.get_user_by_email(session, email)

    # Autenticar usuario
    async def authenticate(self, session: AsyncSession, email: str, password: str) -> User:
        user = await user_crud.get_user_by_email(session, email)
        if not user or not validate_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        return user

    # Listar todos los usuarios
    async def get_all_users(self, session: AsyncSession):
        users = await user_crud.get_users(session)
        if not users:
            raise HTTPException(
                status_code=404,
                detail="No users registered"
            )
        return users

    # Actualizar usuario
    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None
    ) -> User:

        user = await self.get_by_id_with_validation(session, user_id)

        if email and email != user.email:
            existing_user = await user_crud.get_user_by_email(session, email)
            if existing_user and existing_user.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            user.email = email

        if name:
            user.name = name

        if password:
            user.password_hash = encrypt_password(password)

        return await user_crud.update_user(session, user)

    # Eliminar usuario
    async def delete_user(self, session: AsyncSession, user_id: int) -> None:
        user = await self.get_by_id_with_validation(session, user_id)
        await user_crud.delete_user(session, user)


# Instancia global
user_service = UserService()
