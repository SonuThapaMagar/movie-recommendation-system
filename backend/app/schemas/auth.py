from pydantic import BaseModel,Field,ConfigDict

# Data received when a user registers
class UserResgister(BaseModel):
    username:str=Field(min_length=3,max_length=50)
    email:str=Field(min_length=5,max_length=255)
    password:str=Field(min_length=8,max_length=128)

#Response Data
class UserResponse(BaseModel):
    id:int
    username:str
    email:str
    
    model_config=ConfigDict(from_attributes=True)