from sqlalchemy import Column, Integer, String,DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True,comment="Id único del usuario")
    username = Column(String(50),unique=True,index=True,nullable=False,comment="Nombre de usuario único")
    hashed_password = Column(String(255), nullable=False, comment="contrasena hasheada del usuario")
    create_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Fecha y hora de creación del usuario ")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Fecha y hora de la actualización")
    
    @validates('username')
    def validate_username(self,key,username):
        if not username:
            raise ValueError("El nombre de usuario no puede estar vacío")
        if len(username)< 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        if len(username)> 50:
            raise ValueError("El nombre de usuario no puede exceder los 50 caracteres")
        if not username.replace("_", "").replace("-","").isalnum():
            raise ValueError("El nombre de usuario solo debe contener letras,números,guiones y guiones bajos")
        return username.lower().strip()
    
    @validates('hashed_password')
    def validates_hashed_password(self,key,hashed_password):
        if not hashed_password:
            raise ValueError("La contraseña hasheada no puede estar vacía")
        return hashed_password
    
    def __repr__(self):
        return f"<User(id={self.id}, username= '{self.username}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.create_at.isoformat() if self.create_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }