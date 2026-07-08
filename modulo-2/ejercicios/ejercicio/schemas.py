from pydantic import BaseModel, Field,validator,ConfigDict
from typing import Optional

VALID_STATUS = ["pendiente","en_progreso","completado"]

class TaskCreate(BaseModel):
    title:str = Field(...,min_length= 5)
    descripcion: Optional[str] = Field(None,max_length=200)
    status:str= "pendiente"
    priority: int = Field(...,ge=1,le=3)
    
    @validator("status")
    def validate_title(cls, value):
        if value not in VALID_STATUS:
            raise ValueError("Status incorrecto")
        return value

class TaskUpdate(BaseModel):
    title:Optional[str] = Field(...,min_length= 5)
    descripcion: Optional[str] = Field(None,max_length=200)
    status:Optional[str]= "pendiente"
    priority:Optional[int] = Field(...,ge=1,le=3)
    
    @validator("status")
    def validate_status(cls, value):
        if value is None:
            return value
        if value not in VALID_STATUS:
            raise ValueError("Status incorrecto")
        return value
    
class TaskResponse(BaseModel):
    id:int
    title:str
    descripcion:Optional[str]
    status:str
    priority:int
    
    model_config = ConfigDict(from_attributes=True)
                
    