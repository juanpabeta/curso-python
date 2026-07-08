from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from auth.auth_service import hashear_password,verificar_password
from auth.auth_handler import crear_token
from auth.dependencies import get_current_user
from schemas.user_schemas import UserCreate,UserLogin,UserResponse,Token,LoginResponse,Message

router = APIRouter(tags = ['autenticacion'])

@router.post("/login",response_model= LoginResponse,summary="Iniciar sesión" )
def login(data:UserLogin,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user or not verificar_password(data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail= "credencial inválida")
    
    token = crear_token({"sub":user.username})
    
    return LoginResponse(
        access_Token=token,
        token_type= "bearer",
        user = UserResponse.model_validate(user)
    )
    
@router.post("/register",response_model=UserResponse,status_code=201,summary="Registrar nuevo usuario")
def register (data:UserCreate,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    
    if user:
        raise HTTPException(status_code=400,detail= "Usuario ya existe")
    
    hashed = hashear_password(data.password)
    
    nuevo_usuario = User(
        username=data.username,
        hashed_password=hashed
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return UserResponse.model_validate(nuevo_usuario)