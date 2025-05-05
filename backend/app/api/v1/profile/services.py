from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

async def get_user_profile(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def update_user_profile(user_id: int, update_data: dict, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user