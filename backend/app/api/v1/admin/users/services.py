from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.core.security import hash_password
from fastapi import HTTPException, status
from .schemas import AdminUserCreate, AdminUserUpdate

async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user_admin(user_data: AdminUserCreate, db: AsyncSession):
    if user_data.role not in ["Admin", "Customer"]:
        raise HTTPException(status_code=400, detail="Invalid role. Role must be 'Admin' or 'Customer'.")

    existing_user = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='Email already exists')
    
    new_user = User(
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        email = user_data.email,
        hashed_password = hash_password(user_data.password),
        role = user_data.role
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user_admin(user_id: int, user_data: AdminUserUpdate, db: AsyncSession):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.model_dump(exclude_unset=True)  # Use model_dump instead of dict
    if "role" in update_data and update_data["role"] not in ["Admin", "Customer"]:
        raise HTTPException(status_code=400, detail="Invalid role. Role must be 'Admin' or 'Customer'.")

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user_admin(user_id: int, db: AsyncSession):
    user = await get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    return True

async def list_users_admin(db: AsyncSession):
    result= await db.execute(select(User))
    return result.scalars().all()