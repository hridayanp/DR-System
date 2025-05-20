# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import engine, Base
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.admin.users.routes import router as admin_user_router
from app.api.v1.profile.routes import router as profile_router
from app.api.v1.db_connect.routes import router as db_connect_router


from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.exception_handlers import (
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler
)

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

# Register custom handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Register routes
app.include_router(auth_router)
app.include_router(admin_user_router)
app.include_router(profile_router)
app.include_router(db_connect_router)

@app.get("/")
async def root():
    return {"message": "DR System API is running"}