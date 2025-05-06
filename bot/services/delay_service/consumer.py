import json
import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

logger = logging.getLogger(__name__)


class SucsessAddConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            bot: Bot,
            subject_consumer: str,
            stream: str
    ) -> None:
        self.nc = nc
        self.js = js
        self.bot = bot
        self.subject_consumer = subject_consumer
        self.stream = stream

    async def start(self) -> None:
        # можно так же указывать deliver_policy
        # (all, last, new, by_start_sequence)
        self.stream_sub = await self.js.subscribe(
            subject=self.subject_consumer,
            stream=self.stream,
            cb=self.sucsess_add,
            manual_ack=True
        )

    async def sucsess_add(self, msg: Msg):
        payload = json.loads(msg.data)
        await msg.ack()

        with suppress(TelegramBadRequest):
            await self.bot.send_message(
                chat_id=payload['user_id'],
                text='Welcome!'
            )



    # не обязательно, но можно гибко использовать
    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
            logger.info('Consumer unsubscriber')
