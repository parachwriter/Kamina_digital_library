from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User
from typing import List, Optional


#obtener todos

async def get_users(db: AsyncSession)-> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()   #type: ignore

# obtener por email
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


#obtener por id
async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

#Crear usuario
async def create_user(db: AsyncSession, user: User) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

#Actualizar usuario

async def update_user(db: AsyncSession, user: User) -> User:
    await db.commit()
    await db.refresh(user)
    return user

#Borrar usuario

async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()