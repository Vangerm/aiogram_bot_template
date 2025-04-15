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
class Config:
    tg_bot: TgBot
    nats: NatsConfig


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
        )
    )
