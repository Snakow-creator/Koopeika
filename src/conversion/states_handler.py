from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import conf, profile
from core.exceptions import BadMessageText, ValueNotFoundError
from users import user_req

from keyboards import con, main_menu
from states import conversion_state
from conversion.converter import Conversion
from tasks.logger import log

from utils import (checker_value, int_or_float, delete_message,
                   choise_value, checker_num)


router = Router()


# Conversion
@router.message(conversion_state.input_crypto)
async def input_crypto(message: Message, state: FSMContext):
    try:
        user_value = message.text.upper()
        log.debug(user_value)
        value = await checker_value(user_value)


        await state.set_state(conversion_state.input_number)  # install state
        user_id = message.from_user.id
        prof = profile.get(user_id)
        user_obj = await user_req.load(user_id)
        user = user_obj.user
        action = prof.con_choise
        if action == "con":
            answer_, text = await choise_value(value)
            prof.con_value = value  # save first value

            conf.msg[user_id] = await message.answer(
                f"{text}\nУкажите количество валюты, которое вы хотите конвертировать:"
                f"\nИли нажмите на число ниже⬇️",
                reply_markup=con.input_numbers(conf.values_symbols[user["style"]].get(value, f" {value}")),
            )
        elif action == "endcon":
            amount = prof.amount
            user_obj = await user_req.load(user_id)
            user = user_obj.user

            # get two values and convert it
            first_value = prof.con_value
            result = await Conversion.conversion(user_id, first_value, value, amount, conf.rates)
            from_symbol = conf.values_symbols[user["style"]].get(first_value, f" {first_value}")
            to_symbol = conf.values_symbols[user["style"]].get(value, f" {value}")
            log.debug(f"Conversion {message.from_user.id}")
            await message.answer(result.text(from_symbol, to_symbol))
    except ValueNotFoundError as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)


@router.message(conversion_state.input_number)
async def con_input_second_number(message: Message, state: FSMContext):
    try:
        await delete_message(message)
        user_id = message.from_user.id
        prof = profile.get(user_id)
        value = prof.con_value
        user_obj = await user_req.load(user_id)
        user = user_obj.user
        premium_user = await user_obj.premium()

        if value == "⭐️":
            keyboard = con.stars_popular_values(premium_user)
        else:
            keyboard = con.popular_values(premium_user, "endcon")

        await checker_num(message.text, value, premium_user)
        # after checker
        amount = await int_or_float(message.text)
        prof.amount = amount

        await message.answer(
            f"Вы указали: <b>{amount:,}{conf.values_symbols[user['style']].get(value, f' {value}')}</b>."
            f"\nВыберите валюту, в которую требуется конвертировать сумму⬇️",
            reply_markup=keyboard,
        )
    except BadMessageText as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)

    finally:
        await state.clear()





