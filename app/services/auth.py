from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import validate_password, issue_token
from app.crud import user_crud


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await user_crud.get_user_by_email(db, email)
    if not user or not validate_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def login(db: AsyncSession, email: str, password: str):
    user = await authenticate_user(db, email, password)
    access_token = issue_token(payload={"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
