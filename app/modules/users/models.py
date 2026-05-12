from sqlalchemy import Column, Index, Integer, String, func
from core.database import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(50), unique=True)
    email : Mapped[str] = mapped_column(String(256), unique=True, index=True)
    password : Mapped[str] = mapped_column(String(256))
    date_joined: Mapped[datetime] = mapped_column(server_default=func.now())