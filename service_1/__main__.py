import asyncio
import logging.config

from service_1.loger.logging_settings import logging_config
from service_1.config_data.config import load_config
from service_1.utils.nats_connect import connect_to_nats
from service_1.utils.start_consumer import (
    start_do_user_active,
    start_do_user_inactive
)


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info('Starting microservice')

    # Получаем конфигурационные данные
    config = load_config()

    stream = config.stream_config.stream

    # Подключаемся к NATS
    nc, js = await connect_to_nats(servers=config.nats.servers)

    try:
        await asyncio.gather(
            start_do_user_active(
                nc=nc,
                js=js,
                subject_consumer=config.stream_config.subject_admin_dk_consumer,
                subject_publisher=config.stream_config.subject_admin_dk_publisher,
                stream=stream
            ),
            start_do_user_inactive(
                nc=nc,
                js=js,
                subject_consumer=config.stream_config.subject_user_dk_consumer,
                stream=stream
            )
        )
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info('Stop microservice')
    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем соединение с NATS
        await nc.close()
        logger.info('Connection to NATS closed')


if __name__ == '__main__':
    asyncio.run(main())
