# app/db/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/DRSystemDB")

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session for async queries
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base class for ORM models
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session