from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.movies import router as movie_router

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