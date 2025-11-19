from __future__ import annotations
from typing import Optional
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    publication_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    author: Mapped["Author"] = relationship("Author", back_populates="books")  # type: ignore

    borrower_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    borrower: Mapped[Optional["User"]] = relationship("User", back_populates="books")  # type: ignore
