from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str
    birthday: date
    extra_data: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True