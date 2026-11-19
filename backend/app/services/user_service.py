from sqlalchemy.orm import Session
from app.models.user import User
from app.models.rating import Rating
from app.models.favorite import Favorite
from app.models.watchlist import WatchList

def get_user_profile(db: Session, user_id: int):

    return db.query(User).filter(
        User.id == user_id
    ).first()
    
    
def update_user_profile(db:Session,user_id:int,update_data:dict):
    user=get_user_profile(db,user_id)
    if not user:
        return None, "User not found"
    
    # Check for duplicate username
    if "username" in update_data:
        username=update_data["username"]
        if username is None:
            return None,"Username cannot be null"

        
        existing_username=db.query(User).filter(User.username==username,User.id !=user_id).first()
        if existing_username:
            return None,"Username already exists"
        
    # Check for duplicate email
    if "email" in update_data:
        email = update_data["email"]

        if email is None:
            return None, "Email cannot be null"

        existing_email = db.query(User).filter(
            User.email == email,
            User.id != user_id
        ).first()

        if existing_email:
            return None, "Email already exists"
        
        # Update only the supplied fields
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user, None

#Delete user
def delete_user_account(db:Session,user_id:int):
    user=get_user_profile(db,user_id)
    if not user:
        return False
    
    #Delete user specific data
    db.query(Rating).filter(Rating.user_id==user_id).delete(synchronize_session=False)
    
    db.query(Favorite).filter(
        Favorite.user_id == user_id
    ).delete(synchronize_session=False)

    db.query(WatchList).filter(
        WatchList.user_id == user_id
    ).delete(synchronize_session=False)

    #Delete user
    db.delete(user)
    db.commit()
    
    return True