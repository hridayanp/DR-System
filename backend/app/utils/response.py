from typing import Any, Optional

def response_format(
    status: str,
    message: str,
    data: Optional[Any] = None,
    error_code: Optional[str] = "",
    error_message: Optional[str] = ""
) -> dict:
    return {
        "status": status,
        "message": message,
        "data": data,
        "error_code": error_code,
        "error_message": error_message
    }