from sqlalchemy import Column, Integer, String,DateTime,Text
from datetime import datetime
from database import Base

class Producto(Base):
    __tablename__ ="Productos"
    id = Column(Integer, primary_key=True, index=True),
    nombre = Column(String,nullable= False),
    descripcion = Column(Text,nullable= False),
    stock = Column(Integer,nullable=False) 

    
