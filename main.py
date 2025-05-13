from typing import Optional, Annotated
from uuid import uuid4

from fastapi import FastAPI, Query, Path, HTTPException, status, Depends
from sqlalchemy.orm import Session
import uvicorn

from models import Contact, get_db
from pydantic_models import ContactModel, ContactModelResponse


app = FastAPI()


@app.post("/contacts/", tags=["Contacts"], summary="Додати новий контакт", status_code=status.HTTP_201_CREATED, response_model=ContactModelResponse)
async def add_contact(contact_model: ContactModel, db: Session = Depends(get_db)):
    contact = Contact(**contact_model.model_dump(), id=uuid4().hex)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
