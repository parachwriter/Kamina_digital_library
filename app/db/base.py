
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# export explícito
__all__ = ["Base"]
