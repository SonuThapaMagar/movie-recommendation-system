from sqlalchemy.orm import Session, joinedload
from app.models.favorite import Favorite
from app.models.movie import Movie

def add_favorite(db: Session, user_id: int, movie_id: int):
    movie = db.query(Movie).filter(
        Movie.movie_id == movie_id
    ).first()

    if not movie:
        return None, "Movie not found"

    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.movie_id == movie_id
    ).first()

    if existing_favorite:
        return None, "Movie is already in favorites"

    favorite = Favorite(
        user_id=user_id,
        movie_id=movie_id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite, None

def get_user_favorites(db: Session, user_id: int):
    return (
        db.query(Favorite)
        .options(joinedload(Favorite.movie))
        .filter(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .all()
    )

def remove_favorite(db: Session, user_id: int, movie_id: int):
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.movie_id == movie_id
    ).first()

    if not favorite:
        return False

    db.delete(favorite)
    db.commit()

    return True