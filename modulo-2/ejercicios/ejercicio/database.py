from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "PostgreSQL://user:postgres@localhost:5432/task_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocomit = False,
    autoflush= False,
    bind = engine
)

Base = declarative_base()
 

