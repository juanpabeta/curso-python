from pydantic import BaseModel,EmailStr
from typing import Optional


class UserCreate(BaseModel):
    id:int
    name:str
    email:EmailStr
    
    class Config:
        from_atributes = True
        
class TaskCreate(BaseModel):
    title:str
    description:str
    completed:Optional[bool] = False
    user_id = int
    
class TaskCreate(BaseModel):
    id:int
    title:str
    description:str
    completed:Optional[bool] = False
    user_id = int
    
    class Config:
        from_atributes = True