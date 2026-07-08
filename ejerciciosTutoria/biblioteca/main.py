from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import session
from db import SessionLocal,engine,Base
from models import Libro
from scemas import LibroCreate,LibroResponse

Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Libreria",version=1.0)

try:
    db = SessionLocal()
    print("Conexión a la base de datos exitosa")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}") 
    
finally:
    db.close()
