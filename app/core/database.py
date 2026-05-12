from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQL_DB_URL = 'sqlite:///./db.db'
engine = create_engine(SQL_DB_URL,connect_args={"check_same_thread": False})

session_local = sessionmaker(bind=engine,autoflush=False,autocommit=False)

class Base(DeclarativeBase):
    pass