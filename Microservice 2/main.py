from fastapi import FastAPI

from auth_routes import auth_router
from book_routes import book_router
from library_user_routes import library_user_router

app = FastAPI(
    title="Microservice 2 - Library Service",
    description="Microservico de biblioteca com JWT, rate limit e RabbitMQ.",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(library_user_router)
app.include_router(book_router)
