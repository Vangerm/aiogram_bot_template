import json
import logging
import csv
import random

from service_1.services.delay_service.publisher import (
    sucsess_add_user_publisher
    )

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

logger = logging.getLogger(__name__)

# брокеры сообщений - консьюмеры

# получение списка всех дк
class DoUserActiveConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            subject_consumer: str,
            subject_publisher: str,
            stream: str
    ) -> None:
        self.nc = nc
        self.js = js
        self.subject_consumer = subject_consumer
        self.subject_publisher = subject_publisher
        self.stream = stream

    # консьюмер ловящий данные
    async def start(self) -> None:
        # нужно так же указывать deliver_policy
        # (all, last, new, by_start_sequence)
        self.stream_sub = await self.js.subscribe(
            subject=self.subject_consumer,
            stream=self.stream,
            cb=self.do_user_active,
            manual_ack=True
        )

    async def do_user_active(self, msg: Msg) -> None:
        payload = json.loads(msg.data)
        await msg.ack()

        try:
            # добавление в БД и статс активен
            await sucsess_add_user_publisher(
                self.js,
                payload['user_id'],
                self.subject_publisher)

            logger.debug(f'Пользоватль {payload['user_name']} активен')

        except KeyboardInterrupt:
            logger.info('stop by keyboard')
        except Exception as e:
            logger.exception(e)

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info('Consumer unsubscribe')


# получение списка выданных промокодов
class DoUserInactiveConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            subject_consumer: str,
            stream: str
    ) -> None:
        self.nc = nc
        self.js = js
        self.subject_consumer = subject_consumer
        self.stream = stream

    # консьюмер ловящий данные
    async def start(self) -> None:
        # нужно так же указывать deliver_policy
        # (all, last, new, by_start_sequence)
        self.stream_sub = await self.js.subscribe(
            subject=self.subject_consumer,
            stream=self.stream,
            cb=self.do_user_inactive,
            manual_ack=True
        )

    # получение данных из бд
    async def do_user_inactive(self, msg: Msg) -> None:
        payload = json.loads(msg.data)
        await msg.ack()

        try:
            # изменение статуса пользователя на неактивен в БД
            logger.debug(f'Пользоватль {payload['user_name']} не активен')

        except KeyboardInterrupt:
            logger.info('stop by keyboard')
        except Exception as e:
            logger.exception(e)

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info('Consumer unsubscribe')
