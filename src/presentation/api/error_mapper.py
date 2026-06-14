from fastapi import HTTPException

from src.domain.exceptions.domain_exception import DomainException


def to_http_error(error: Exception) -> HTTPException:
    if isinstance(error, PermissionError):
        return HTTPException(status_code=403, detail=str(error))

    if isinstance(error, ValueError):
        return HTTPException(status_code=404, detail=str(error))

    if isinstance(error, DomainException):
        return HTTPException(status_code=400, detail=str(error))

    return HTTPException(status_code=500, detail="Internal server error.")