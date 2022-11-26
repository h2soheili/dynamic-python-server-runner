import json
from asyncio import AbstractEventLoop
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from typing import Optional, Callable, Tuple, Any

from app.enums import KafkaTopics
from app.utils.global_log import log_factory

logger = log_factory.get_logger(__name__)


class KafkaClient(object):

    def __init__(self, loop: AbstractEventLoop, url: str, group_id: str):
        self.loop = loop
        self.url = url
        self.group_id = group_id
        self.consumer = None
        self.producer = None
        self.consumer_is_running = False

    async def start_consumer(self, topic: KafkaTopics):
        logger.info('starting consumer')
        # await asyncio.sleep(1)
        try:
            self.consumer = AIOKafkaConsumer(
                topic.value,
                loop=self.loop,
                bootstrap_servers=self.url,
                # group_id=self.group_id
            )
            await self.consumer.start()
            logger.info('consumer started')
            self.consumer_is_running = True
        except Exception as e:
            self.consumer_is_running = False
            logger.error('start_consumer failed: ', error=e)

    async def consume(self, pulling_interval: int = 1, on_new_event_received: Callable = None, auto_commit=True):
        logger.info('starting consume events', consumer_is_running=self.consumer_is_running)
        while self.consumer_is_running:
            logger.info('consumer is running ...')
            try:
                # some delay for decrease cpu usage
                await asyncio.sleep(pulling_interval)
                result = await self.consumer.getmany(timeout_ms=10 * 1000)
                logger.info('consumer result ', result=result)
                for tp, messages in result.items():
                    if messages:
                        for msg in messages:
                            logger.warn("consumed message: ", msg=msg.value.decode())
                            logger.warn("on_new_event_received: ", on_new_event_received=on_new_event_received)
                            if on_new_event_received is not None:
                                on_new_event_received(msg)
                if auto_commit:
                    await self.consumer.commit()
            except Exception as e:
                # self.consumer_is_running = False
                logger.error('consume events failed: ', error=e)

    async def produce(self, topic: KafkaTopics, value: Any):
        try:
            await self.producer.start()
            await self.producer.send_and_wait(topic.value, value=json.dumps(value).encode())
        except Exception as e:
            logger.error('produce: ', error=e)

    async def start_producer(self):
        logger.info('starting producer')
        try:
            self.producer = AIOKafkaProducer(loop=self.loop,
                                             bootstrap_servers=self.url)
            await self.producer.start()
            logger.info('producer started')
        except Exception as e:
            logger.error('start_producer: ', error=e)

    async def stop_producer(self):
        try:
            await self.producer.stop()
        except Exception as e:
            logger.error('stop_producer: ', error=e)
