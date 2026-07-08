from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..schemas import UserCreate
from ..models import UserDB

router = APIRouter

@router.post("/users",status_code=201)
def create_user(user:UserCreate):
    
    db: Session = SessionLocal()
    existing_user = db.query(UserDB).filter(
        UserDB.email == user.email  
    ).first()
    
    if existing_user: 
        db.close()
        raise HTTPException(
            status_code= 409,
            detail = "usuario existente"
            
        )
    new_user = UserDB(
        name = user.name,
        email = user.email
    )
    db.close()
    
    return new_user

"""
#Crear mas de un usuario 
@router.post("/users/bulk", status_code=201)
def create_users(users_list: List[User]):
    existing_emails = [u.email for u in users]
    # Validar duplicados (tanto existentes como dentro del mismo envío)
    new_emails = []
    for user in users_list:
        if user.email in existing_emails or user.email in new_emails:
            raise HTTPException(status_code=409, detail=f"Email duplicado: {user.email}")
        new_emails.append(user.email)
    users.extend(users_list)
    return users_list"""
    
@router.get("/users/{user_id}")
def get_user(user_id:int):
    db: Session = SessionLocal()
    user = db.query(UserDB).filter(
        UserDB.id == user_id
            )
    
    