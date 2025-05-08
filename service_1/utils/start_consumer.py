import logging

from service_1.services.delay_service.consumer import (
    DoUserActiveConsumer,
    DoUserInactiveConsumer
)

from nats.aio.client import Client
from nats.js.client import JetStreamContext


logger = logging.getLogger(__name__)


async def start_do_user_active(
        nc: Client,
        js: JetStreamContext,
        subject_consumer: str,
        subject_publisher: str,
        stream: str
        ) -> None:
    logger.debug(f'subject: {subject_consumer}, stream: {stream}')
    consumer = DoUserActiveConsumer(
        nc=nc,
        js=js,
        subject_consumer=subject_consumer,
        subject_publisher=subject_publisher,
        stream=stream
    )
    logger.info('Start poll dk info consumer')
    await consumer.start()


async def start_do_user_inactive(
        nc: Client,
        js: JetStreamContext,
        subject_consumer: str,
        stream: str
        ) -> None:
    logger.debug(f'subject: {subject_consumer}, stream: {stream}')
    consumer = DoUserInactiveConsumer(
        nc=nc,
        js=js,
        subject_consumer=subject_consumer,
        stream=stream
    )
    logger.info('Start poll dk info consumer')
    await consumer.start()
