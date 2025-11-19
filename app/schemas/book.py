from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from fastapi import Query


# Create Book

class CreateBook(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=100, 
        json_schema_extra={"examples": ["El Viejo y el Mar"]}
    )
    publication_year: Optional[int] = Field(
        None, ge=0, 
        json_schema_extra={"examples": [2001]}
    )
    author_id: int = Field(
        ..., 
        json_schema_extra={"examples": [312]}
    )

    model_config = ConfigDict(from_attributes=True)


# Update Book

class UpdateBook(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=100, 
        json_schema_extra={"examples": [ "El Principito"]}
    )
    publication_year: Optional[int] = Field(
        None, ge=0, 
        json_schema_extra={"examples": ["value"]}
    )
    author_id: Optional[int] = Field(
        None, 
        json_schema_extra={"examples": [4321]}
    )

    model_config = ConfigDict(from_attributes=True)


# Output Book

class BookOut(BaseModel):
    id: int
    title: str
    publication_year: Optional[int]
    author_id: int
    borrower_id: Optional[int]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1984,
                "title": "Firewalls don't Stop Dragons",
                "publication_year": 1,
                "author_id": 123,
                "borrower_id": 333
            }
        }
    )


# Search Book

class SearchBook(BaseModel):
    title: Optional[str] = None
    author_name: Optional[str] = None
    year: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Función de dependencia para parámetros query
def SearchBookDep(
    title: Optional[str] = Query(None, examples=[ "El Principito"]),
    author_name: Optional[str] = Query(None, examples=[ "Agatha Christie"]),
    publication_year: Optional[int] = Query(None, examples=[ 2008])
) -> SearchBook:
    return SearchBook(title=title, author_name=author_name, year=publication_year)


# Search Book Output

class SearchBookOut(BaseModel):
    id: int
    title: str
    publication_year: Optional[int]
    author_name: str
    borrower_id: Optional[int]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 222,
                "title": "El Principito",
                "publication_year": 1943,
                "author_name": "Antoine de Saint-Exupéry",
                "borrower_id": 2
            }
        }
    )
