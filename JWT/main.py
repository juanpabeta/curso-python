from fastapi import(
    FastAPI,
    HTTPException,
    Depends,
    Request
)

from fastapi.responses import JSONResponse


from auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

import logging

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# CREAR APP

app = FastAPI()


#USUARIO FALSO

fake_user = {
    "username": "maria",
    "password": hash_password("123456"),
    "role": "admin"
}

# RUTA PRINCIPAL

@app.get("/")
def home():

    logger.info("Acceso a HOME")

    return{
        "message":"API funcionando"
    }

# LOGIN

@app.post("/login")
def login(
    username: str,
    password: str
):
    # VALIDAR USUARIO

    logger.info(
        f"Intento de login: {username}"
    )

    if username != fake_user["username"]:

        logger.warning(
            f"Usuario incorrecto: {username}"
        )
        
        raise HTTPException(
            status_code=401,
            detail="Usuario incorrecto"
        )
    
    # VALIDAR PASSWORD

    password_valid = verify_password(
        password,
        fake_user["password"]
    )

    if not password_valid:

        logger.warning(
            f"contraseña incorrecta para: {username}"
        )
        raise HTTPException(
            status_code=401,
            detail="contraseña incorrecta"
        )
    
    #GENERAR EL TOKEN

    access_token = create_access_token({
        "sub": username,
        "role":fake_user["role"]
    })

    logger.info(
        f"Login exitoso: {username}"
    )

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }

# RUTA PROTEGIDA

@app.get("/profile")
def profile(token: str):

    logger.info(
        f"Intento de login a /profile"
    )

    payload = verify_token(token)

    logger.info(
        f"Token valido para el usuario: {payload.get('sub')}"
    )

    return{
        "message": "Ruta protegida",
        "user": payload
    }

#RUTA SOLO ADMIN

@app.get("/admin")
def admin_route(token: str):
    logger.info(
        "Intento de acceso a /admin"
    )

    payload = verify_token(token)

    #VALIDAR ROL

    if payload ["role"] != "admin":
        logger.warning(
            f"Acceso denegado para usuario: {payload.get('sub')}"
            
        )

        raise HTTPException(
            status_code=403,
            detail= "No tiene permisos")
    
    logger.info(
        f"Acceso admin permitido para {payload.get('sub')}"
    )

    return {
        "menssage": "Bienvenido administrador",
        "user": payload
    }

# MANEJO GLOBAL DE ERRORES

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Error interno del servidor"
        }
    )