from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from config import conf
from base.keyboard import start_keyboard


router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(
        text=(
            "<b>Здравствуйте! Я Koopeika🧑🏻‍💼\n"
            "Бот революционной конвертации валют.\n"
            "Нажмите на одну из кнопок ниже, чтобы начать работу👇</b>"
        ),
        reply_markup=start_keyboard(),
    )


@router.message(Command("info"))
async def info(message: Message):
    await message.answer(conf.terms_of_service)
