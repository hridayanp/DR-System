from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db
from app.core.security import require_admin
from app.models.user import User
from .schemas import AdminUserCreate, AdminUserUpdate, AdminUserOut
from .services import create_user_admin, list_users_admin, get_user_by_id, update_user_admin, delete_user_admin
from app.utils.response import response_format

router = APIRouter(prefix='/admin/users', tags=['Admin'])

@router.post('/', response_model=dict)
async def create_user(user_data: AdminUserCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    user = await create_user_admin(user_data, db)
    return response_format("success", "User created successfully", {"email": user.email, "role": user.role})

@router.get('/', response_model=dict)
async def get_users(db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    users = await list_users_admin(db)
    return response_format("success", "User list fetched", [AdminUserOut.from_orm(user) for user in users])

@router.get('/{user_id}', response_model=dict)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return response_format("success", "User fetched", AdminUserOut.from_orm(user))

@router.put('/{user_id}', response_model=dict)
async def update_user(user_id: int, user_data: AdminUserUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    user = await update_user_admin(user_id, user_data, db)
    return response_format("success", "User updated", AdminUserOut.from_orm(user))

@router.delete('/{user_id}', response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)):
    await delete_user_admin(user_id, db)
    return response_format("success", f"User with id {user_id} deleted", None)