from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)
    Base = declarative_base()
except SQLAlchemyError as e:
    raise Exception(f"Error al conectar con la base de datos: {str(e)}")    

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error operando la bd:{str(e)} ")
    finally:
        db.close()