from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.services.service_contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactCreate, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.create(body)

@router.get("/", response_model=List[ContactResponse])
async def get_all_contacts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.get_all(skip, limit)

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    contact = await service.get_by_id(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    contact = await service.update(contact_id, body)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    contact = await service.delete(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.search(query)

@router.get("/birthdays/upcoming", response_model=List[ContactResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    service = ContactService(db)
    return await service.upcoming_birthdays()