from typing import Any


def success_response(message: str, data: Any = None, meta: dict | None = None) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
        "meta": meta if meta is not None else {},
    }


def error_response(message: str, code: str, errors: dict | None = None) -> dict:
    return {
        "success": False,
        "message": message,
        "errors": errors if errors is not None else {},
        "code": code,
    }
