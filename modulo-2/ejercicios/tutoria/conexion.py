import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session=Session()
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
Base.metadata.create_all(engine)
def crear_usuario(nombre, email):
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    session.add(nuevo_usuario)
    session.commit()
    print("usuario creado: ", nuevo_usuario.id, nuevo_usuario.nombre, nuevo_usuario.email)
    
def leer_usuarios():
    usuarios = session.query(Usuario).all()
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Nombre: {usuario.nombre}, Email: {usuario.email}")
def actualizar_usuario(usuario_id, nuevo_nombre=None, nuevo_email=None):
    usuario = session.query(Usuario).filter_by(id=usuario_id).first()
    if usuario:
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre
        if nuevo_email:
            usuario.email = nuevo_email
        session.commit()
        print(f"Usuario actualizado: ID: {usuario.id}, Nombre: {usuario.nombre}, Email: {usuario.email}")
    else:
        print("Usuario no encontrado.")
def eliminar_usuario(usuario_id):
    usuario = session.query(Usuario).filter_by(id=usuario_id).first()
    if usuario:
        session.delete(usuario)
        session.commit()
        print(f"Usuario eliminado: ID: {usuario.id}, Nombre: {usuario.nombre}, Email: {usuario.email}")
    else:
        print("Usuario no encontrado.")
