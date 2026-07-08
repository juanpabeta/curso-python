from pydantic import BaseModel

class LibroBase(BaseModel):
    titulo:str
    autor:str
    
class LibroCreate(LibroBase):
    pass

class LibroResponse():
    id:int
    
    class Config:
        orm_mode = True