import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

from src.db.db import get_db
from src.db.models import User
from src.schemas import UserCreate, UserResponse, Token, LoginModel
from src.services.service_auth import register_user, pwd_context, create_access_token, get_current_user
from src.repository.repo_users import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)



@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing = await repo.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
    return await register_user(user, repo)

@router.post("/login", response_model=Token)
async def login(form: LoginModel, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_email(form.email)
    if not user or not pwd_context.verify(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
async def get_me(request: Request, current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/avatar")
async def upload_avatar_route(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    temp_path = f"temp/{current_user.id}_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    from src.services.service_cloudinary import upload_avatar
    avatar_url = await upload_avatar(temp_path, public_id=f"user_avatars/{current_user.id}")
    os.remove(temp_path)

    updated_user = await UserRepository(db).update_avatar(current_user, avatar_url)
    return {"avatar_url": updated_user.avatar_url}