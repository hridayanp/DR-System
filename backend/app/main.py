# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Startup: Check DB connection
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connected successfully.")
    except SQLAlchemyError as e:
        print("❌ Database connection failed:", str(e))
    
    yield  # Let the app run
    
    # 🔻 Shutdown (optional): You can add cleanup code here
    print("🛑 App is shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "DR System API is running"}