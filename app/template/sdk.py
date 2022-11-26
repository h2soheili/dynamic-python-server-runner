import time
from starlette.websockets import WebSocketDisconnect
import websockets
from .main import settings
from .logger import log_factory

logger = log_factory.get_logger(__name__)
user_id = settings.USER_ID
script_name = settings.SCRIPT_NAME


def watch_ticker(ticker_key: str, cb):
    if cb:
        cluster_key = get_ticker_cluster_key(ticker_key)
        with websockets.connect(f"ws://localhost:6000/{cluster_key}/{ticker_key}/{user_id}") as websocket:
            try:
                while True:
                    data = websocket.recv()
                    time.sleep(0.3)
                    cb(data)
            except WebSocketDisconnect:
                logger.error('watch_ticker WebSocketDisconnect', ticker_key=ticker_key, user_id=user_id,
                             script_name=script_name)
            except Exception as error:
                logger.error('watch_ticker Exception', error=error, ticker_key=ticker_key, user_id=user_id,
                             script_name=script_name)
    else:
        logger.error('watch_ticker no callback provided', ticker_key=ticker_key)


def get_ticker_cluster_key(ticker_key: str) -> str:
    time.sleep(0.2)
    return 'crypto.top'


def callback(message):
    logger.info('watch_ticker callback', message=message)


# watch_ticker('BITCOIN', callback)


def get_daily_historical_data(ticker_key: str, from_data: str, to_date):
    time.sleep(1)
    return []


def get_historical_data(ticker_key: str, from_data: str, to_date):
    time.sleep(1)
    return []


