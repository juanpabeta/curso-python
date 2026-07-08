from sqlalchemy import Column,Integer,String,JSON,ForeignKey,Float
from database import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer,primary_key=True,index=True)
    nombre = Column(String,nullable=False,index= True)
    notas = Column(JSON)
    
class Notas(Base):
    __tablename__ = "notas"
    id = Column(Integer,primary_key=True,index=True)
    valor = Column(Float,nullable=False)
    
    estudiantes_id = Column(Integer,ForeignKey("estudiantes.id"))
