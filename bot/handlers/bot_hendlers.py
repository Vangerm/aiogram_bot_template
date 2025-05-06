import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states.states import PromocodeFillForm
# from fluentogram import TranslatorRunner


logger = logging.getLogger(__name__)

bot_router = Router()

# демонстрация форм с состояниями

@bot_router.message(Command(commands='cancel'), StateFilter(PromocodeFillForm))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='1'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.set_state()


@bot_router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(
        text='2'
        )
    await state.set_state()


@bot_router.message(Command(commands='aaa'))
async def process_autopost_command(message: Message, state: FSMContext):
    await message.answer(text='3')
    await state.set_state(PromocodeFillForm.fill_1)


@bot_router.message(StateFilter(PromocodeFillForm.fill_1),
                    lambda x: x.text.isdigit())
async def process_autopost_id_vk_group(message: Message, state: FSMContext):
    await state.update_data(a_1=int(message.text))
    await message.answer(
        text='4'
    )
    await state.set_state(PromocodeFillForm.fill_2)


@bot_router.message(StateFilter(PromocodeFillForm.fill_1))
async def warning_not_id_vk_group(message: Message):
    await message.answer(
        text='5'
    )


@bot_router.message(StateFilter(PromocodeFillForm.fill_2),
                    lambda x: x.text.isdigit())
async def process_autopost_id_tg_group(message: Message, state: FSMContext):
    await state.update_data(a_2=int(message.text))

    data_state = await state.get_data()

    await state.clear()

    await message.answer(
        text=f'{data_state}'
    )


@bot_router.message(StateFilter(PromocodeFillForm.fill_2))
async def warning_not_id_tg_group(message: Message):
    await message.answer(
        text='6'
    )
