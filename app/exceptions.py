from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


class UserAlreadyRegistered(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="El usuario ya existe")


class BookNotAvailable(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="El libro se encuentra prestado")


class AuthorHasBooks(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="El autor tiene libros asociados")


class NotFound(HTTPException):
    def __init__(self, entity: str = "Recurso"):
        super().__init__(status_code=404, detail=f"{entity} no encontrado")


def register_exception_handler(app: FastAPI):

    @app.exception_handler(UserAlreadyRegistered)
    async def user_exist_handler(request: Request, exc: UserAlreadyRegistered):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "message": exc.detail}
        )

    @app.exception_handler(BookNotAvailable)
    async def book_not_available_handler(request: Request, exc: BookNotAvailable):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "message": exc.detail}
        )

    @app.exception_handler(AuthorHasBooks)
    async def author_has_books_handler(request: Request, exc: AuthorHasBooks):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "message": exc.detail}
        )

    @app.exception_handler(NotFound)
    async def not_found_handler(request: Request, exc: NotFound):
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "message": exc.detail}
        )


#al final no usé esto