from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List

app= FastAPI()

#Modelo de datos
class User(BaseModel):
    id: int 
    name: str
    email: EmailStr

#Base de datos simulada
users: List[User] = []

#Crear usuario
@app.post("/users", status_code=201)
def create_user(user: User):
    for u in users:
        if u.email == user.email:
            raise HTTPException(status_code=409, detail="Email ya existe")
        
    users.append(user)
    return user

#Crear mas de un usuario 

@app.post("/users/bulk", status_code=201)
def create_users(users_list: List[User]):
    existing_emails = [u.email for u in users]

    # Validar duplicados (tanto existentes como dentro del mismo envío)
    new_emails = []

    for user in users_list:
        if user.email in existing_emails or user.email in new_emails:
            raise HTTPException(status_code=409, detail=f"Email duplicado: {user.email}")
        new_emails.append(user.email)

    users.extend(users_list)
    return users_list

#Listar usuarios
@app.get("/users")
def get_users():
    return users


#Obtener usuarios por ID
@app.get("/users/{user_id}")
def get_users(user_id:int):
    for user in users:
        if user.id == user_id:
            return user
        
#Actualizar usuario
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return updated_user

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return {"message": "Usuario eliminado"}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")