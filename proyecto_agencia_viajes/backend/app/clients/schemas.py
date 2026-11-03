from pydantic import BaseModel, EmailStr, ConfigDict, Field

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150) 
    phone: str = Field(..., min_length=1, max_length=50)
    email: EmailStr | None = None


class CompanionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    phone: str = Field(..., min_length=1, max_length=50)


class ClientResponse(ClientCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CompanionResponse(CompanionCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ClientUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    phone: str | None = Field(None, min_length=1, max_length=50)
    email: EmailStr | None = None
    
class CompanionUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    phone: str | None = Field(None, min_length=1, max_length=50)
   
