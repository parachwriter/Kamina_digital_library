from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator
from datetime import datetime
from typing import Optional
from app.core.password_types import UserPassword
from app.core.password_rules import check_password_strength

# ---------------------------
# Base schema (reutilizable)
# ---------------------------
class UserSchemaBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: UserPassword

    @field_validator("password")
    def validate_password_security(cls, pswrd: str) -> str:
        return check_password_strength(pswrd)

# ---------------------------
# Schema para crear usuario
# ---------------------------
class UserCreate(UserSchemaBase):
    pass  # hereda name, email y password

# ---------------------------
# Schema para actualizar usuario
# ---------------------------
class UpdateUser(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[UserPassword] = None

    @field_validator("password")
    def validate_password_security(cls, pswrd: Optional[str]) -> Optional[str]:
        if pswrd is None:
            return pswrd
        return check_password_strength(pswrd)

# ---------------------------
# Schema para salida (response)
# ---------------------------
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("registered_at")
    def format_registered_at(self, value: datetime):
        return value.strftime("%d-%m-%Y")

# ---------------------------
# Schema para login
# ---------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str
