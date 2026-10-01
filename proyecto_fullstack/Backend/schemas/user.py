from pydantic import BaseModel, EmailStr, ConfigDict,Field
from datetime import datetime
 

class UsuarioCreate(BaseModel):
    nombre_completo: str = Field(...,min_length=3,max_length=50,description="nombre completo del usuario", examples=["Juan Pablo Medina Betancourt"])   
    email: EmailStr = Field(...,description="Dirreción de correo del usuario",example="Juan@gmail.com") 

class UsuarioResponse(BaseModel):
    id: int
    nombre_completo:str
    email:EmailStr
    fecha_registro: datetime
 
    model_config = ConfigDict(from_attributes=True)
    
