from passlib.context import CryptContext
from src.schemas import UserCreate
from src.repository.repo_users import UserRepository
from src.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(user: UserCreate, repo: UserRepository) -> User:
    hashed_password = pwd_context.hash(user.password)
    return await repo.create_user(user.email, hashed_password)