from sqlalchemy import Column, Integer, String
from db import Base

class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)