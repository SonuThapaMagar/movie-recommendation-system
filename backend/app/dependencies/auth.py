from fastapi import HTTPException,Depends,status #dependency injection=depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

import jwt
from jwt.exceptions import InvalidTokenError

from app.database.database import get_db
from app.models.user import User
from app.utils.security import SECRET_KEY,ALGORITHM

# Extracts the Bearer token from the request header.
bearer_scheme=HTTPBearer()

def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(bearer_scheme),
    db:Session=Depends(get_db)
):
    token=credentials.credentials
    
    try:
        # Verify the token and decode its payload
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        # Extract user ID from the JWT subject.
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError("Token subject is missing")
        
        if not isinstance(user_id, str) or not user_id.isdigit():
            raise InvalidTokenError("Invalid user ID")

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    # Find the user in the database.
    user=db.query(User).filter(User.id==int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    return user