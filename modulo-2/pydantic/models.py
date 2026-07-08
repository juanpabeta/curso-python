from pydantic import BaseModel,Field

class CreateTask(BaseModel):
    titulo:str = Field(...,min_length=3,max_length=50)
    descripcion:str = Field(...,min_length=10,max_length=200)
    prioridad:int = Field(...,ge=1,le=5)
    completada:bool = False
    
class UpdateTask(BaseModel):
    titulo:str | None = Field(...,min_length=3,max_length=50)
    descripcion:str | None= Field(...,min_length=10,max_length=200)
    prioridad:int | None= Field(...,ge=1,le=5)
    completada:bool |None= None
    
class ReponseTask(BaseModel):
    id:int
    titulo:str
    descripcion:str 
    prioridad:int 
    completada:bool 
    
    
    