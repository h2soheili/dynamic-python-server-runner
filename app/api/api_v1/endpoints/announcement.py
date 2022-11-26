import json
from asyncio import sleep
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.redis_client import redis_pubsub, redis_client
from app.enums import EventTypes
from app.utils.global_log import log_factory

router = APIRouter()
logger = log_factory.get_logger(__name__)


@router.get("/", response_model=Any)
async def get(tracing_no: int,
              ) -> Any:
    some_heavy_work(tracing_no, '10')
    await sleep(10)
    """
    Retrieve instances.
    """
    return {}


def some_heavy_work(tracing_no: int, client_id: Any):
    data = {"tracing_no": tracing_no, "result": 200, "client_id": client_id}
    data = json.dumps(data)
    redis_client.publish(EventTypes.ReProcess.value, data)
