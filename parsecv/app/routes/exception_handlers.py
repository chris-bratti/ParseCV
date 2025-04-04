from app.models import HealthException, ParsingException
from fastapi import Request
from fastapi.responses import JSONResponse


async def health_exception_handler(request: Request, exc: HealthException):
    return JSONResponse(
        status_code=500,
        content={
            "status": "down",
            "services": {"Extractor": exc.extractor_status},
            "message": exc.message,
        },
    )


async def parse_exception_handler(request: Request, exc: ParsingException):
    return JSONResponse(
        status_code=exc.status, content={"success": False, "message": exc.message}
    )
