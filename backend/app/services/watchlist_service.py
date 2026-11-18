from sqlalchemy.orm import Session,joinedload

from app.models.movie import Movie
from app.models.watchlist import WatchList

def add_to_watchlist(db:Session,user_id:int,movie_id:int):
    #check whether movie exists
    movie=db.query(Movie).filter(Movie.movie_id==movie_id).first()
    
    if not movie_id: return None, "Movie not found"
    
    #check whether movie is already in user's watchlist
    existing_item=db.query(WatchList).filter(WatchList.user_id==user_id,WatchList.movie_id==movie_id).first()
    if existing_item: return None,"Movie is already in watchlist"
    
    # Create a new watchlist entry
    watchlist_item=WatchList(user_id=user_id,movie_id=movie_id)
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)
    
    return watchlist_item,None

def get_user_watchlist(db:Session,user_id:int):
    return (
        db.query(WatchList)
        .options(joinedload(WatchList.movie))
        .filter(WatchList.user_id==user_id)
        .order_by(WatchList.created_at.desc())
        .all()
    )
    
def remove_from_watchlist(db: Session, user_id: int, movie_id: int):
    watchlist_item = db.query(WatchList).filter(
        WatchList.user_id == user_id,
        WatchList.movie_id == movie_id
    ).first()

    if not watchlist_item:
        return False

    db.delete(watchlist_item)
    db.commit()

    return True