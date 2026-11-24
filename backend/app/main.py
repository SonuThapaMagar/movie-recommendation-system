from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from app.utils.exception_handlers import(http_Exception_handler,validation_exception_handler)
from app.routes.movies import router as movie_router
from app.routes.auth import router as auth_router
from app.routes.favorites import router as favorite_router
from app.routes.watchlist import router as watchlist_router
from app.routes.ratings import router as rating_router
from app.routes.users import router as user_router
from app.routes.recommendations import router as recommendation_router

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
app.include_router(watchlist_router)
app.include_router(rating_router)
app.include_router(user_router)
app.include_router(recommendation_router)

app.add_exception_handler(
    HTTPException,
    http_Exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)