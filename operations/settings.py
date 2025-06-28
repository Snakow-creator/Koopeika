import commands.keyboards as kb
import database.online_config as oc
import database.requests as rq


async def text_settings():
    return "Выбери параметр который хочешь изменить."


async def change_time_zone(callback=None):
    await callback.answer("")
    text = (
        ""
        "Тебе дано на выбор около 27 разных часовых поясов, \n"
        "выбери тот который тебе удобен.\n"
        "Если не понимаешь что такое UTC, или не знаешь какой тебе часовой пояс выбрать, "
        'ты можешь ознакомиться <a href="https://ru.wikipedia.org/wiki/Список_часовых_поясов_по_странам">здесь</a>'
        ""
    )
    await callback.message.edit_text(
        text=text, reply_markup=kb.clbk.time_zone(), disable_web_page_preview=True
    )


async def clbk_time_zone_edit(action, tg_id):
    await rq.time_zone_edit(action, tg_id)
    text = f"Вы изменили часовой пояс на <b>UTC{action}</b>"
    return text


async def clbk_value_edit(action, tg_id):
    await rq.value_edit(action, tg_id)
    text = f"Вы изменили валюту на <b>{action}</b>"
    return text


async def clbk_fiat_amount_edit(action, tg_id):
    await rq.fiat_amount_edit(action, tg_id)
    text = f"Вы изменили кол-во чисел после запятой(фиат) на <b>{action}</b>"
    return text


async def clbk_crypto_amount_edit(action: int, tg_id):
    await rq.crypto_amount_edit(action, tg_id)
    text = f"Вы изменили кол-во чисел после запятой(криптовалюта) на <b>{action}</b>"
    return text


async def clbk_info(callback):
    await callback.answer("")
    user = await rq.user_get(callback.from_user.id)
    await callback.message.edit_text(
        f"Информация:\n"
        f"➖➖➖➖➖\n"
        f"Часовой пояс: <b>{user.time_zone}</b>\n"
        f"Установленная валюта: <b>{user.value}</b>\n"
        f"Стиль валют: <b>{oc.styles_keys[user.style]}</b>\n"
        f"Кол-во чисел после запятой(фиат): <b>{user.fiat_amount}</b>\n"
        f"Кол-во чисел после запятой(крипта): <b>{user.crypto_amount}</b>"
    )


async def clbk_style(callback):
    await callback.answer("")
    await callback.message.edit_text(
        "Выбери стиль отображения валют."
        "\n1. Символы - более красивое отображение."
        "\n2. Названия - более информативное"
        "\nПример:"
        "\nUSD - $ (Символы)"
        "\nUSD - USD 🇺🇸 (Названия)",
        reply_markup=kb.clbk.change_style(),
    )
