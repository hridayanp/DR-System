from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db
from app.models.user import User
from app.core.security import get_current_user
from .schemas import ProfileOut, ProfileUpdate
from .services import get_user_profile, update_user_profile
from app.utils.response import response_format

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=dict)
async def view_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await get_user_profile(current_user.id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return response_format("success", "Profile fetched", ProfileOut.model_validate(user))

@router.put("/", response_model=dict)
async def update_profile(
    update_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await update_user_profile(current_user.id, update_data.model_dump(exclude_unset=True), db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return response_format("success", "Profile updated", ProfileOut.model_validate(user))