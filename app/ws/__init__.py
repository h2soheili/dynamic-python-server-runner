import json
import time
from asyncio import sleep
import asyncio
from typing import Dict
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.core.loop import get_loop
from app.core.redis_client import redis_client, redis_pubsub
from app.enums import EventTypes
from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)


class ConnectionManager:
    def __init__(self):
        self.clients: Dict[str, WebSocket] = dict()

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.clients[client_id] = websocket
        logger.info('on connect', clients=self.clients, )

    def disconnect(self, client_id: str):
        if client_id in self.clients:
            self.clients.get(client_id).close()
            self.clients.pop(client_id)

    async def send_message_to(self, client_id: str, message: str):
        logger.info('send_message_to', clients=self.clients, )
        logger.info('send_message_to', client_id=client_id, message=message)
        if client_id in self.clients:
            try:
                await self.clients.get(client_id).send_text(message)
            except Exception as error:
                logger.error('ws send_message_to', error=error)

    async def broadcast(self, message: str):
        for key, connection in self.clients.items():
            await connection.send_text(message)


manager = ConnectionManager()


async def run_ws(app: FastAPI):
    """
        subscribe + listen loop

    """
    redis_pubsub.subscribe(EventTypes.ReProcess.value)
    asyncio.ensure_future(listen_to_redis())

    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: str):
        await manager.connect(client_id, websocket, )
        try:
            pass
            while True:
                await sleep(1.5)
                data = await websocket.receive_text()
                await manager.send_message_to(client_id, data)
        except WebSocketDisconnect:
            manager.disconnect(client_id)
            logger.error('WebSocketDisconnect')
        except Exception as error:
            logger.error('ws Exception', error=error)


async def listen_to_redis():
    await sleep(1)
    while True:
        await sleep(2)
        try:
            msg = redis_pubsub.get_message()
            logger.info('redis_pubsub.get_message', msg=msg)
            if msg and "data" in msg:
                logger.info('redis_pubsub.get_message 22', data=msg.get('data'))
                data = json.loads(msg.get('data'))
                await manager.send_message_to(data.get('client_id'), json.dumps(data))
        except Exception as error:
            logger.error('redis_pubsub.get_message', error=error)
