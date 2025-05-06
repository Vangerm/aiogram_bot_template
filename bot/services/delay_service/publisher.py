import json

from nats.js.client import JetStreamContext


async def user_active(
        js: JetStreamContext,
        user_id: int,
        user_name: str,
        subject: str
) -> None:

    payload = json.dumps({
        'user_id': user_id,
        'user_name': user_name
    }).encode()

    await js.publish(subject=subject, payload=payload)


async def user_inactive(
        js: JetStreamContext,
        user_id: int,
        user_name: str,
        subject: str
) -> None:

    payload = json.dumps({
        'user_id': user_id,
        'user_name': user_name
    }).encode()

    await js.publish(subject=subject, payload=payload)
