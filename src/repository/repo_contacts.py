from typing import List, Any, Coroutine, Sequence
from datetime import date, timedelta

from sqlalchemy import select, or_, func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate

class ContactRepository:
    def __init__(self, db: AsyncSession, user:User):
        self.db = db
        self.user = user

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Contact]:
        stmt = select(Contact).where(Contact.user_id == self.user.id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, contact_id: int) -> Contact | None:
        return await self.db.get(Contact, contact_id)

    async def create(self, body: ContactCreate) -> Contact:
        contact = Contact(**body.model_dump())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update(self, contact_id: int, body: ContactUpdate) -> Contact | None:
        contact = await self.get_by_id(contact_id)
        if contact:
            for field, value in body.model_dump().items():
                setattr(contact, field, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete(self, contact_id: int) -> Contact | None:
        contact = await self.get_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search(self, query: str) -> Sequence[Contact]:
        stmt = select(Contact).where(
            Contact.user_id == self.user.id).where(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def upcoming_birthdays(self) -> Sequence[Contact]:
        today = date.today()
        end = today + timedelta(days=7)
        stmt = select(Contact).where(
            Contact.user_id == self.user.id).where(
            func.date_part('doy', Contact.birthday).between(
                func.date_part('doy', today),
                func.date_part('doy', end)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()