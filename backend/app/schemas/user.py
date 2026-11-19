from pydantic import BaseModel,ConfigDict,EmailStr,Field

class UserUpdate(BaseModel):
    username:str|None=Field(default=None,min_length=3,max_length=50)
    email:str|None=None
    
class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)