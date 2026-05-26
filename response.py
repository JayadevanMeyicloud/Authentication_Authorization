
from fastapi import HTTPException


def success_response(message, data=None):

    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message):

    raise HTTPException(
        status_code=400,
        detail=message
    )