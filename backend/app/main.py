# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import engine, Base
from app.api.v1.auth.routes import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ DB connected and tables created")
    except Exception as e:
        print("❌ DB connection failed:", e)
    yield
    # Shutdown actions (if any)
    print("👋 Shutting down")

# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Register routes
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "DR System API is running"}