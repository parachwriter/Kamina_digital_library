from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from typing import Optional
from datetime import date, datetime

class BaseAuthor(BaseModel): 
    birth_date: Optional[date] = Field(
        None,
        description="Date of birth using the following format dd/mm/yyyy",
        json_schema_extra={"example": "17/02/2002"}
    )
    model_config = ConfigDict(from_attributes=True)

    @field_validator("birth_date", mode="before")
    def validate_date(cls, rawdate):
        if rawdate is None:
            return rawdate
        if isinstance(rawdate, str):
            try:
                return datetime.strptime(rawdate, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("The date must be in the following format dd/mm/yyyy")
        return rawdate            

    @field_serializer("birth_date")
    def serialize_date(self, value: date) -> Optional[str]:
        if value is None:
            return None
        return value.strftime("%d/%m/%Y")


# Create
class CreateAuthor(BaseAuthor):
    name: str = Field(..., json_schema_extra={"example": "Anna Aleksevna"})


# Update
class UpdateAuthor(BaseAuthor):
    name: Optional[str] = Field(None, json_schema_extra={"example": "Anna Aleksevna"})


# Out
class AuthorOut(BaseAuthor):
    id: int
    name: str = Field(..., json_schema_extra={"example": "Juan Paramo"})
