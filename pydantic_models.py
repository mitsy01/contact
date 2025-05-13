import re
from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator


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
    
    

    