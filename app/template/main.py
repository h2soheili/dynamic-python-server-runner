from typing import Optional, Dict, Any
from fastapi import FastAPI
from pydantic import BaseSettings
import importlib
from .logger import log_factory


class Settings(BaseSettings):
    USER_ID: Optional[str] = None
    SCRIPT_NAME: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()

server_name = f"{settings.USER_ID}/{settings.SCRIPT_NAME}"

app = FastAPI(title=server_name)

logger = log_factory.get_logger(__name__)


@app.get("/")
def read_root():
    return {"server_name": server_name}


@app.on_event("startup")
async def startup_event():
    logger.info('startup event ...', settings=settings)
    try:
        script = importlib.import_module('script', 'run_script')
        script.run_script(settings.USER_ID, settings.SCRIPT_NAME)
    except Exception as error:
        logger.error('run_script', error=error)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info('server shutdown', settings=settings)
