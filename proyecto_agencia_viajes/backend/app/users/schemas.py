from pydantic import BaseModel, ConfigDict,Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    is_active: bool = Field(default=True)
    
    
class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
    
    
class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=100)
    password: str | None = Field(None, min_length=8, max_length=100)
    is_active: bool | None = None
    
    
