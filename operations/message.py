from aiogram.types import Message

import database.online_config as oc

async def message_update(message: Message, text, keyboard=None):
    if keyboard:
        oc.msg[message.from_user.id] = await message.answer(text, reply_markup=keyboard)
    else:
        oc.msg[message.from_user.id] = await message.answer(text)


async def delete_message(message: Message):
    msg = oc.msg.get(message.from_user.id)
    await message.delete()
    await msg.delete()
