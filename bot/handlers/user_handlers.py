import logging
from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.fsm.context import FSMContext
from aiogram.filters import (
                            Command,
                            CommandStart,
                            ChatMemberUpdatedFilter,
                            KICKED)
# from fluentogram import TranslatorRunner

from bot.services.delay_service.publisher import user_active, user_inactive


logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(
                                message: Message,
                                state: FSMContext,
                                js,
                                subject_user_active_publisher: str
                                ):
    await state.clear()
    logger.info(f'{message.chat.username} ({message.chat.id}) - start bot')
    await user_active(
        js=js,
        user_id=message.chat.id,
        user_name=message.chat.username,
        subject=subject_user_active_publisher
    )

@user_router.message(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_kicked_user(
                                message: ChatMemberUpdated,
                                state: FSMContext,
                                js,
                                subject_user_inactive_publisher: str
                                ):
    await state.clear()
    logger.info(f'{message.chat.username} ({message.chat.id}) - kicked bot')
    await user_inactive(
        js=js,
        user_id=message.chat.id,
        user_name=message.chat.username,
        subject=subject_user_inactive_publisher
    )

@user_router.message(Command(commands='help'))
async def process_help_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='help'
        )
