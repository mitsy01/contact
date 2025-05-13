import os
from typing import Optional
from uuid import uuid4

from sqlalchemy import String, create_engine, Text
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv


load_dotenv()
SQLALCHEMY_URI = os.getenv("SQLALCHEMY_URI")
engine = create_async_engine(SQLALCHEMY_URI, echo=True)
Base = declarative_base()


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
    

# Base.metadata.create_all(bind=engine)

async def get_db():
    with Session(bind=engine) as session:
        yield session
        
        
        