import os
from datetime import datetime,timedelta,timezone

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30"))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not configured")

def create_access_token(user_id:int):
    expires_at=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload={
        "sub":str(user_id), #stores user is as token subject
        "exp":expires_at #tells JWT when the token expires
    }
    
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM) #signs the token using your secret key
    return token