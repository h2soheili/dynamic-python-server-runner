from asyncio import AbstractEventLoop
import asyncio
from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)


def get_loop() -> AbstractEventLoop:
    loop = None
    # loop = asyncio.get_running_loop()
    # return loop
    try:
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        # loop = asyncio.get_running_loop()
        # loop = asyncio.get_running_loop()
    except RuntimeError as e:
        logger.error('  get_loop', error=e)
        loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_forever()
    finally:
        # loop.run_forever()
        return loop
