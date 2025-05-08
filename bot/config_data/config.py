from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class NatsStreamConfig:
    stream: str

    subject_active_publisher: str
    subject_inactive_publisher: str

    subject_sucsess_add_consumer: str


@dataclass
class Config:
    tg_bot: TgBot
    nats: NatsConfig
    nats_stream: NatsStreamConfig


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
        ),
        nats=NatsConfig(
            servers=env.list('NATS_SERVERS')
        ),
        nats_stream=NatsStreamConfig(
            stream=env('NATS_STREAM_CONSUMERS'),

            subject_active_publisher=env('NATS_ACTIVE_PUBLISHER_SUBJECT'),
            subject_inactive_publisher=env('NATS_INACTIVE_PUBLISHER_SUBJECT'),

            subject_sucsess_add_consumer=env('NATS_ACTIVE_CONSUMER_SUBJECT')
        )
    )
