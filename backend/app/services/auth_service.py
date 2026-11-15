from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.models.user import User

#Password hasher
password_hash=PasswordHash.recommended()

def register_user(
    db:Session,
    username:str,
    email:str,
    password:str
):
    #Email normalization
    email=email.strip().lower()
    
    # Check if username already exists
    existing_username= db.query(User).filter(User.username==username).first()
    if existing_username: return None,"Username already exists"
    
    #Check if email exists
    existing_email=db.query(User).filter(User.email==email).first()
    if existing_email: return None,"Email already exists"
    
    #Password hash
    hashed_password=password_hash.hash(password)
    
    #Create new user
    new_user=User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user,None
    except Exception:
        db.rollback()
        raise
