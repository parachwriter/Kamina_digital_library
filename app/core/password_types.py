from typing import Annotated
from pydantic import StringConstraints

UserPassword = Annotated[str, StringConstraints(min_length=4, max_length=32)]#pa mas seguridad