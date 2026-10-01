from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime
from db.db import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer,primary_key=True,index=True,autoincrement = True)
    nombre_completo = Column(String(50),nullable= False)
    email = Column(String(50),nullable = 50,unique = True)
    fecha_registro = Column(DateTime(timezone=True),default=datetime.now)