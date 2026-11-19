from datetime import datetime,timezone
from sqlalchemy.orm import Session,joinedload

from app.models.rating import Rating
from app.models.movie import Movie

def add_or_update_rating(
    db: Session,
    user_id: int,
    movie_id: int,
    rating_value: float
):    #check whether movie exists
    movie=db.query(Movie).filter(Movie.movie_id==movie_id).first()
    
    if not movie: return None, "Movie not found"
    
    # Check whether this user has already rated this movie
    existing_rating = db.query(Rating).filter(
    Rating.user_id == user_id,
    Rating.movie_id == movie_id
    ).first()
    
    if existing_rating:
        #Update rating
        existing_rating.rating=rating_value
        existing_rating.timestamp=int(datetime.now(timezone.utc).timestamp())
        
        db.commit()
        db.refresh(existing_rating)
        
    
    #create new rating
    new_rating=Rating(
        user_id=user_id,
        dataset_user_id=None,
        movie_id=movie_id,
        rating=rating_value,
        timestamp=int(datetime.now(timezone.utc).timestamp())
    )
    
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    
    return new_rating,True,None

def get_user_ratings(db:Session,user_id:int):
    return(
        db.query(Rating)
        .options(joinedload(Rating.movie))
        .filter(Rating.user_id==user_id)
        .order_by(Rating.timestamp.desc())
        .all()
    )
    
def get_user_movie_rating(db:Session,user_id:int,movie_id:int):
    return(
        db.query(Rating)
        .options(joinedload(Rating.movie))
        .filter(
            Rating.user_id==user_id,
            Rating.movie_id==movie_id
        )
        .first()
    )
    
def delete_user_rating(db:Session,user_id:int,movie_id:int):
    rating=db.query(Rating).filter(Rating.user_id==user_id,Rating.movie_id==movie_id).first()
    
    if not rating: return False
    
    db.delete(rating)
    db.commit()
    
    return True