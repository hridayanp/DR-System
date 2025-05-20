# app/api/v1/db_connect/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.core.security import get_current_user
from app.api.v1.db_connect.schemas import DBConnectionRequest
from app.api.v1.db_connect.services import test_user_db_connection
from app.utils.response import response_format
from app.models.user import User

router = APIRouter(prefix="/db-connect", tags=["Database Connect"])

@router.post("/test", response_model=dict)
async def test_connection(
    db_data: DBConnectionRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        metadata = await test_user_db_connection(db_data)
        return response_format(
            status="success",
            message="Connection successful.",
            data={
                "db_type": db_data.db_type,
                "host": db_data.host,
                "port": db_data.port,
                "database": db_data.database,
                "tables": metadata
            }
        )
    except SQLAlchemyError as e:
        return response_format(
            status="error",
            message="Database connection failed.",
            error_code="DB_CONN_ERROR",
            error_message=str(e)
        )
    except Exception as e:
        return response_format(
            status="error",
            message="Unexpected error occurred.",
            error_code="UNEXPECTED_ERROR",
            error_message=str(e)
        )






