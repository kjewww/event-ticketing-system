from fastapi import HTTPException

from src.domain.exceptions.domain_exception import DomainException


def to_http_error(error: Exception) -> HTTPException:
    message = str(error)

    if isinstance(error, PermissionError):
        return HTTPException(status_code=403, detail=message)

    if isinstance(error, DomainException):
        return HTTPException(status_code=400, detail=message)

    if isinstance(error, ValueError):
        lowered = message.lower()

        if "not found" in lowered:
            return HTTPException(status_code=404, detail=message)

        return HTTPException(status_code=400, detail=message)

    return HTTPException(status_code=500, detail="Internal server error.")