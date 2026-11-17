from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from app.utils.exception_handlers import(http_Exception_handler,validation_exception_handler)
from app.routes.movies import router as movie_router
from app.routes.auth import router as auth_router
from app.routes.favorites import router as favorite_router

app=FastAPI(title="Movie Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/")
def home():
    return {"message": "Movie Recommendation API is running"}

app.include_router(movie_router)
app.include_router(auth_router)
app.include_router(favorite_router)

app.add_exception_handler(
    HTTPException,
    http_Exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)