from datetime import datetime, timedelta, UTC

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_async_db




# Configuración de seguridad

oauth_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

password_ctx = CryptContext(
    schemes=["argon2"], #mas nuevo
    deprecated="auto"
)

JWT_SECRET = settings.SECRET_KEY
JWT_ALGO = "HS512" #mas seguro 
TOKEN_LIFETIME_MIN = 30

def encrypt_password(raw_password: str) -> str:
    return password_ctx.hash(raw_password)


def validate_password(raw: str, hashed_pswrd: str) -> bool:
    return password_ctx.verify(raw, hashed_pswrd)



# Token JWT
def issue_token(payload: dict, duration: timedelta | None = None) -> str:
    data = payload.copy()
    expiration_time = datetime.now(UTC) + (
        duration or timedelta(minutes=TOKEN_LIFETIME_MIN)
    )
    data["exp"] = expiration_time

    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)


def parse_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )



# Obtener usuario autenticado

async def get_current_user(
    token: str = Depends(oauth_bearer),
    session: AsyncSession = Depends(get_async_db)
):
    # Import dentro de la función para romper el ciclo
    from app.services.user_service import user_service

    data = parse_token(token)

    user_id = data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin información válida",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = await user_service.get_by_id_with_validation(session, int(user_id))

    return user
