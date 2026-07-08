from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    name = Column(String)
    email = Column(String, unique= True)
    
    task = relationship("TaskDB", back_populates= "user")
    
class TaskDB(Base):
    __tablename__ = "task"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column(String)
    completada = Column(Boolean)
    id_user = Column(Integer,ForeignKey("users.id"))
    
    