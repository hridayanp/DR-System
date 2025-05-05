from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from fastapi.responses import JSONResponse
from app.utils.response import response_format


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = [
        f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()
    ]
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_format(
            status="error",
            message="Validation Error",
            error_code="VALIDATION_ERROR",
            error_message="; ".join(error_messages),
            data=None
        )
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    error_map = {
        HTTP_401_UNAUTHORIZED: "Unauthorized access",
        HTTP_403_FORBIDDEN: "Forbidden",
        HTTP_404_NOT_FOUND: "Resource not found"
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=response_format(
            status="error",
            message="HTTP Exception",
            error_code=f"HTTP_{exc.status_code}",
            error_message=error_map.get(exc.status_code, str(exc.detail)),
            data=None
        )
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_format(
            status="error",
            message="Internal Server Error",
            error_code="INTERNAL_SERVER_ERROR",
            error_message=str(exc),
            data=None
        )
    )