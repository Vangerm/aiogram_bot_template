import json

from nats.js.client import JetStreamContext
# from tenacity import retry # библиотека для повторных отправок сообщений

# брокеры сообщений - паблишеры

# Отправка приглашения пользователю
# @retry
async def sucsess_add_user_publisher(
        js: JetStreamContext,
        chat_id: int,
        subject: str
) -> None:

    payload = json.dumps({
        'chat_id': chat_id
    }).encode()

    await js.publish(subject=subject, payload=payload)
