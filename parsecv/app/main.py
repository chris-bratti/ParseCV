import uvicorn
from app.logging_config import logger
from app.models import HealthException, ParsingException
from app.routes import health_exception_handler, parse_exception_handler
from app.routes import health_router as health_router
from app.routes import router as parse_router
from app.services.text_extrator_service import healthcheck
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.include_router(parse_router, prefix="/api")
app.include_router(health_router, prefix="/health")
app.add_exception_handler(HealthException, health_exception_handler)
app.add_exception_handler(ParsingException, parse_exception_handler)


if not healthcheck():
    logger.error("Text Extractor service is unavailable")
else:
    logger.info("Text Extractor service is healthy")


host = "0.0.0.0"
port = 8282
app_name = "app.main:app"

if __name__ == "__main__":
    uvicorn.run(app_name, host=host, port=port)
