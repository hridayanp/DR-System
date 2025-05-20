# app/api/v1/db_connect/schemas.py
from pydantic import BaseModel, Field

class DBConnectionRequest(BaseModel):
    db_type: str = Field(..., example="postgresql")
    host: str = Field(..., example="localhost")
    port: int = Field(..., example=5432)
    username: str = Field(..., example="hridayanphukan")
    password: str = Field(..., example="yourpassword")
    database: str = Field(..., example="DRSystemDB")