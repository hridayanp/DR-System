from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.api.v1.auth.schemas import UserCreate, UserLogin
from fastapi import HTTPException, status

async def create_user(user_data: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def authenticate_user(user_data: UserLogin, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    access_token = create_access_token({'sub': user.email})
    refresh_token = create_refresh_token({'sub': user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}