from aiogram import Router

from . import user_handlers
from . import admin_handlers
from . import bot_hendlers
from . import other_handlers


def get_routers() -> list[Router]:
    return [
        admin_handlers.admin_router,
        user_handlers.user_router,
        other_handlers.other_router  # other_handlers - должен быть последним
    ]
