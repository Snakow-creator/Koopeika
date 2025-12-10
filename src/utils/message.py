from aiogram.types import Message

from config import conf


async def message_update(message: Message, text, keyboard=None):
    if keyboard:
        conf.msg[message.from_user.id] = await message.answer(text, reply_markup=keyboard)
    else:
        conf.msg[message.from_user.id] = await message.answer(text)


async def delete_message(message: Message):
    msg = conf.msg.get(message.from_user.id)
    await message.delete()
    await msg.delete()
