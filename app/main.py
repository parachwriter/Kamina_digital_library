from fastapi import FastAPI
from app.routers import user_router, author_router, book_router, auth
from app.exceptions import register_exception_handler

app = FastAPI()

# Routers
app.include_router(auth.router)
app.include_router(user_router.router)
app.include_router(book_router.router)
app.include_router(author_router.router)

register_exception_handler(app)

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente "}
