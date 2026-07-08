from sqlalchemy import Column, Integer, String,DateTime,Text
from datetime import datetime
from database import Base

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True),
    title = Column(String,nullable= False),
    descripcion = Column(Text,nullable= False),
    status = Column(String,default = "pendiente"),
    priority = Column(String, default=1)
    create_at = Column(DateTime,default=datetime.utcnow )
        