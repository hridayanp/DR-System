from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db
from app.api.v1.auth.schemas import UserCreate, UserLogin, Token
from app.api.v1.auth.services import create_user, authenticate_user
from app.utils.response import response_format

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/signup', response_model=dict)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await create_user(user_data, db)
        return response_format(
            status='success',
            message=f'User {user.email} created successfully',
            data={'email': user.email}
        )
    except Exception as e:
        return response_format(
            status='error',
            message='User signup failed',
            error_code='SIGNUP_ERROR',
            error_message=str(e)
        )


@router.post('/login', response_model=dict)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        token_data = await authenticate_user(user_data, db)

        return response_format(
            status="success",
            message="Login successful.",
            data={
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"]
            }
        )
    except HTTPException as e:
        return response_format(
            status='error',
            message='User login failed',
            error_code='LOGIN_ERROR',
            error_message=str(e)
        )