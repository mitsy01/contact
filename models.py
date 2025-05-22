import os
from typing import Optional
from uuid import uuid4
import asyncio
from enum import Enum, auto
from datetime import datetime, date


from sqlalchemy import String, create_engine, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv


load_dotenv()
SQLALCHEMY_URI = os.getenv("SQLALCHEMY_URI")
engine = create_async_engine(SQLALCHEMY_URI, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


class RoleEnum(Enum):
    admin = auto()
    user = auto()

class Contact(Base):
    __tablename__ = "contacs"
    
    id: Mapped[str] = mapped_column(String(100),primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50))
    adress: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    number: Mapped[str] = mapped_column(String(50))
    account_id: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid4().hex
        
        
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[str] = mapped_column(Boolean(), default=True)
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.user.name)
    token: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid4().hex


class Article(Base):
    __tablename__ = "articles"
        
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(Text())
    author_email: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(100))
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    
    
class Comment(Base):
    __tablename__ = "comments"
        
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    comment: Mapped[str] = mapped_column(String(100))
    author_com: Mapped[str] = mapped_column(String(100))
    created_com: Mapped[datetime] = mapped_column(default=datetime.now())



async def creare_db():
    async with engine.begin() as connection:
       await connection.run_sync(Base.metadata.drop_all)
       await connection.run_sync(Base.metadata.create_all)
     
        
async def get_db():
    async with async_session() as session:
        yield session
        



if __name__ == "__main__":
    asyncio.run(creare_db())