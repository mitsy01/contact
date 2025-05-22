import re
from typing import Optional, Annotated
from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field, field_validator
from models import RoleEnum


class ContactModel(BaseModel):
    first_name: Annotated[str, Field(..., min_length=2, max_length=50, description="Ім'я.")]
    last_name: Annotated[Optional[str], Field(None, max_length=50, description="Прізвище.")]
    email: Annotated[EmailStr, Field(..., min_length=3, max_length=50, description="Email.", examples=["email@a.ua"])]
    adress: Annotated[Optional[str], Field(None, max_length=150, description="Адреса.", examples=["Україна, Харків, вул. Северинопотоцького, будинок 69"])]
    username: Annotated[str, Field(..., min_length=2, max_length=50, description="Nickname.")]
    number: Annotated[str, Field(..., min_length=18,max_length=18, description="Номер телефону.", examples=["+380(92)-228-21-69"])]
    account_id: Annotated[Optional[str], Field(None, description="Посилання на аккаунт.", examples=["https://t.me/example"])]
    
    @field_validator("number")
    def number_validate(cls, value: str):
        if re.search(r"\+380\(\d{2}\)-\d{3}-\d{2}-\d{2}", value):
            return value
        raise ValueError("Номер телефону повинен дотримуватися у форматі: +380(92)-228-21-69")
    
    
class ContactModelResponse(ContactModel):
    id: str
    
class UserModel(BaseModel):
    username: Annotated[str, Field(..., description="Ім'я користувача.", min_length=2, max_length=100)]
    password: Annotated[str, Field(..., description="Пароль.", min_length=10, max_length=100)]
    email: Annotated[EmailStr, Field(..., description="Email.", min_length=2, max_length=100)]
    

class UserModelResponse(UserModel):
    id: str
    is_active: bool
    role: RoleEnum


class ArticleModel(BaseModel):
    titile: Annotated[str, Field(..., description="Заголовок.", min_length=5, max_length=100)]
    author: Annotated[str, Field(..., description="Автор.", min_length=5, max_length=100)]
    author_email: Annotated[EmailStr, Field(..., description="Email автора.", min_length=5, max_length=100)]
    content: Annotated[str, Field(..., description="Зміст статті.", min_length=5, max_length=100)]
    created: Annotated[Optional[datetime], Field(None, description="Дата випуску статті.", default_factory=datetime.now)]
    
    
class ArticleModelResponse(ArticleModel):
    id: str
    created: Annotated[Optional[datetime], Field(description="Дата випуску статті.", default_factory=datetime.now)]
    
    
class CommentModel(BaseModel):
    comment:  Annotated[str, Field(..., description="Зміст коментаря.", min_length=5, max_length=100)]
    author_com:  Annotated[str, Field(..., description="Автор коментаря.", min_length=5, max_length=100)]
    created_com:  Annotated[Optional[datetime], Field(None, description="Дата створення коментаря.", default_factory=datetime.now)]
    

class CommentModelResponse(CommentModel):
    id: str
    created_com:  Annotated[Optional[datetime], Field(None, description="Дата створення коментаря.", default_factory=datetime.now)]