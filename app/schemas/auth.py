from pydantic import BaseModel, EmailStr
from fastapi import Form

class LoginForm(BaseModel):
    email: EmailStr
    password: str

def login_dependency(
        email: EmailStr = Form(...),
        password: str = Form(...)
) -> LoginForm:
    return LoginForm(email=email, password=password)

class JWT(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JWTPayload(BaseModel):
    sub: int  # user_id
    email: EmailStr
