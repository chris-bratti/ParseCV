from app.logging_config import logger
from app.models import HealthException
from app.services.text_extrator_service import healthcheck
from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/status")
async def api_healthcheck():
    if healthcheck():
        return {"status": "up", "services": {"Extractor": "up"}}
    logger.error("App is unhealthy")
    raise HealthException(
        message="Extractor service is unreachable", extractor_status="down"
    )
