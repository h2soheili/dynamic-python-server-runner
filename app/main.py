from fastapi import FastAPI
import asyncio as asyncio
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.api.api_v1.endpoints import html
from app.core.config import settings
from app.core.redis_client import redis_pubsub
from app.enums import EventTypes
from app.utils.global_log import log_factory
from app.ws import run_ws, listen_to_redis

logger = log_factory.get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="description",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=True,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(html.router, tags=["/html"])
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    logger.info('startup event ...')
    # await run_ws(app)
    # asyncio.get_running_loop().run_until_complete(asyncio.create_task(listen_to_redis()))
    # loop = asyncsyncio.get_event_loop()
    # kafka_client = KafkaClient(loop, 'localhost:9092', 'topic1', 'group1')
    # kafka_client.start()
    # await asyncio.sleep(1)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info('shutdown event ...')
    # redis_pubsub.unsubscribe(EventTypes.ReProcess.value)
    await asyncio.sleep(1)


if __name__ == "app.main":
    print('__________________')
