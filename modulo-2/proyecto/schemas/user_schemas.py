from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username:str = Field(...,min_length=3,max_length=50,description="Nombre del usuario único",examples=['juan_perez'])
    password:str = Field(...,min_length=6,description="Contraseña Usuario",examples=["miPassword123"])
    
class UserLogin(BaseModel):
    username:str = Field(...,examples=['juan_perez'])
    password:str = Field(...,min_length=6,description="Contraseña Usuario",examples=["miPassword123"])

class UserResponse(BaseModel):
    id:int = Field(examples=[1])
    username:str = Field(...,examples=['juan_perez'])
    create_at:Optional[datetime] = Field(default=None,examples=["2026-06-8T20:55:00"])
    update_at:Optional[datetime] = Field(default=None,examples=None)
    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_Token: str = Field(...,description="Token JWT de acceso",examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type:str = Field(default="bearer",description="Tipo de token",examples=["bearer"])
    
class LoginResponse(BaseModel):
    access_Token: str = Field(...,description="Token JWT de acceso",examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type:str = Field(default="bearer",description="Tipo de token",examples=["bearer"])
    user:UserResponse = Field(...,description="Datos del usuario autenticado")
    
class Message(BaseModel):
    mensaje:str = Field(examples=['operación realizada de forma exitosa'])
    
    