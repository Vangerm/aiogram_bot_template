import logging

from aiogram import Bot
from bot.services.delay_service.consumer import SucsessAddConsumer

from nats.aio.client import Client
from nats.js.client import JetStreamContext


logger = logging.getLogger(__name__)


async def start_sucsess_add_consumer(
        nc: Client,
        js: JetStreamContext,
        bot: Bot,
        subject_consumer: str,
        stream: str
        ) -> None:
    consumer = SucsessAddConsumer(
        nc=nc,
        js=js,
        bot=bot,
        subject_consumer=subject_consumer,
        stream=stream
    )
    logger.info('Start sucsess add users consumer')
    await consumer.start()
