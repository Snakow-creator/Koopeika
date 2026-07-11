from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import profile, conf
from users import user_req

from tasks.logger import log
from states import balance_state, conversion_state
from keyboards import con, main_menu

from utils.choise_value import choise_value
from conversion.converter import Conversion



router = Router()


# full list value for conversion and assets
@router.callback_query(F.data.startswith("otherlist_value_"))
async def check_fulllist_values(callback: CallbackQuery):
    await callback.answer("")

    action = callback.data.split("_")[-1]
    await callback.message.edit_text("Укажите валюту:", reply_markup=con.full_list_values(action))


@router.callback_query(F.data.startswith("cryptolist_value_"))
async def check_fulllist_values(callback: CallbackQuery):
    await callback.answer("")

    user_obj = await user_req.load(callback.from_user.id)
    max_coins = user_obj.user.get("crypto_max_coins")

    action = callback.data.split("_")[-1]
    await callback.message.edit_text("Укажите валюту:", reply_markup=con.crypto_values(max_coins, action))


# input cryptovalue
@router.callback_query(F.data.startswith("input_crypto_"))
async def input_crypto(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    action = callback.data.split("_")[-1]

    if action == "add":
        log.debug("Change value")
        await state.set_state(balance_state.input_crypto)
    if action in ("con", "endcon"):
        log.debug("Conversion")
        await state.set_state(conversion_state.input_crypto)

    prof = profile.get(callback.from_user.id)
    action = callback.data.split("_")[-1]
    prof.con_choise = action
    prof.tr_message_id = callback.message.message_id
    await callback.message.edit_text(
        "Введите название криптовалюты:" \
        "\n➖➖➖➖➖" \
        "\nУказывайте название пожалуйста в формате <b>кодового названия</b>(например: BTCUSDT, ETHUSDT)",
        reply_markup=con.back_button(action),
    )


# back to popular values
@router.callback_query(F.data.startswith("value_back_"))
async def value_back(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.clear()

    # get user data
    user_obj = await user_req.load(callback.from_user.id)
    premium_user = await user_obj.premium()
    action = callback.data.split("_")[-1]  # input last parametr in callback_data

    text = profile.get(callback.from_user.id).text
    await callback.message.edit_text(text, reply_markup=con.popular_values(premium_user, action))


# conversion choise for telegram stars
@router.callback_query(F.data == "con_value_pop_⭐️")
async def stars_input_value(callback: CallbackQuery, state: FSMContext):

    await state.set_state(conversion_state.input_number)  # install state
    await callback.answer("")
    await callback.message.edit_text(
        "Выберите нужное действие для звёзд⭐️" "\nУчтите, что курс зависит от <b>направления обмена</b>",
        reply_markup=con.stars_choise(),
    )


# save first value, input popular and full list values
@router.callback_query(F.data.startswith("con_value_"))
async def con_input_value(callback: CallbackQuery, state: FSMContext):
    await state.set_state(conversion_state.input_number)  # install state
    prof = profile.get(callback.from_user.id, create=True)
    user_id = callback.from_user.id
    user_obj = await user_req.load(callback.from_user.id)
    user = user_obj.user
    value = callback.data.split("_")[-1]  # input last word in callback_data
    answer_, text = await choise_value(value)
    prof.con_value = value  # save first value

    await callback.answer(answer_)
    conf.msg[user_id] = await callback.message.edit_text(
        f"{text}\nУкажите количество валюты, которое вы хотите конвертировать:"
        f"\nИли нажмите на число ниже⬇️",
        reply_markup=con.input_numbers(
            conf.values_symbols[user["style"]].get(value, f' {value}')
        ),
    )


# get fast input amount value
@router.callback_query(F.data.startswith("con_input_amount_"))
async def con_fast_input_second_value(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    user_id = callback.from_user.id
    prof = profile.get(user_id)
    action = callback.data.split("_")[-1]  # get amount
    value = prof.con_value
    user_obj = await user_req.load(user_id)
    user = user_obj.user
    premium_user = await user_obj.premium()
    prof.amount = int(action)
    prof.text = (
        f"Вы указали: <b>{int(action)}{conf.values_symbols[user['style']].get(value, f' {value}')}</b>."
        f"\nВыберите валюту, в которую требуется конвертировать сумму⬇️"
    )
    if value[0:2] == "⭐️":
        keyboard = con.stars_popular_values(premium_user)
    else:
        keyboard = con.popular_values(premium_user, "endcon")

    await state.clear()
    await callback.message.edit_text(prof.text, reply_markup=keyboard)


# input second value and output result
@router.callback_query(F.data.startswith("endcon_value_"))
async def con_output_result(callback: CallbackQuery):
    await callback.answer("")
    # получаем необходимые данные
    user_id = callback.from_user.id
    prof = profile.get(user_id)
    value = callback.data.split("_")[-1]  # input last word in callback_data
    amount = prof.amount
    user_obj = await user_req.load(user_id)
    user = user_obj.user

    # get two values and convert it
    first_value = prof.con_value
    result = await Conversion.conversion(user_id, first_value, value, amount, conf.rates)
    from_symbol = conf.values_symbols[user["style"]].get(first_value, f" {first_value}")
    to_symbol = conf.values_symbols[user["style"]].get(value, f" {value}")
    log.debug(f"Conversion {callback.from_user.id}")
    await callback.message.edit_text(
        result.text(from_symbol, to_symbol), reply_markup=main_menu
    )
