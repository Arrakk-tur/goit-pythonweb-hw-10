from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.repo_contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate

class ContactService:
    def __init__(self, db: AsyncSession):
        self.repo = ContactRepository(db)

    async def create(self, body: ContactCreate):
        return await self.repo.create(body)

    async def get_all(self, skip: int = 0, limit: int = 100):
        return await self.repo.get_all(skip, limit)

    async def get_by_id(self, contact_id: int):
        return await self.repo.get_by_id(contact_id)

    async def update(self, contact_id: int, body: ContactUpdate):
        return await self.repo.update(contact_id, body)

    async def delete(self, contact_id: int):
        return await self.repo.delete(contact_id)

    async def search(self, query: str):
        return await self.repo.search(query)

    async def upcoming_birthdays(self):
        return await self.repo.upcoming_birthdays()