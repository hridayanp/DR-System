# app/api/v1/db_connect/services.py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect
from app.api.v1.db_connect.schemas import DBConnectionRequest
import urllib.parse

async def test_user_db_connection(db_data: DBConnectionRequest):
    if db_data.db_type == "postgresql":
        driver = "asyncpg"
    elif db_data.db_type == "mysql":
        driver = "aiomysql"
    else:
        raise ValueError("Unsupported database type")

    encoded_password = urllib.parse.quote_plus(db_data.password)
    url = f"{db_data.db_type}+{driver}://{db_data.username}:{encoded_password}@{db_data.host}:{db_data.port}/{db_data.database}"

    engine = create_async_engine(url, echo=False, future=True)
    async with engine.connect() as conn:
        def get_table_names(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()
        table_names = await conn.run_sync(get_table_names)
        return table_names