import commands.keyboards as kb
import database.online_config as oc
import database.requests as rq

from datetime import datetime


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
    await callback.message.edit_text(text, reply_markup=kb.set.time_zone(), disable_web_page_preview=True)


async def time_zone_edit(action, tg_id):
    await rq.Edit.time_zone(tg_id, action)
    text = f"Вы изменили часовой пояс на <b>UTC{action}</b>"
    return text


async def default_value_edit(action, tg_id):
    await rq.Edit.value(tg_id, action)
    text = f"Вы изменили валюту на <b>{action}</b>({oc.values.get(action, action[:3])})"
    return text


async def fiat_amount_edit(action, tg_id):
    await rq.Edit.fiat_amount(tg_id, action)
    text = f"Вы изменили кол-во чисел после запятой(фиат) на <b>{action}</b>"
    return text


async def crypto_amount_edit(action: int, tg_id):
    await rq.Edit.crypto_amount(tg_id, action)
    text = f"Вы изменили кол-во чисел после запятой(криптовалюта) на <b>{action}</b>"
    return text


async def crypto_max_coins_edit(action: int, tg_id: int):
    await rq.Edit.crypto_max_coins(tg_id, action)
    text = f"Вы изменили список валют на <b>{oc.crypto_max_coins[action]}</b>"
    return text


async def settings_user_info(premium, user_id):
    user_obj = await rq.SelectUser.load(user_id)
    user = user_obj.user
    text = (
        f"<b>Информация:</b>\n"
        f"➖➖➖➖➖\n"
        f"Часовой пояс: <b>{user['time_zone']}</b>\n"
        f"Установленная валюта: <b>{user['value']}</b>\n"
        f"Стиль валют: <b>{oc.styles_keys[user['style']]}</b>\n"
        f"Кол-во чисел после запятой(фиат): <b>{user['fiat_amount']}</b>\n"
        f"Кол-во чисел после запятой(крипта): <b>{user['crypto_amount']}</b>\n"
    )
    if premium:
        premium_time = datetime.strftime(user["premium_until"], "%d.%m.%Y %H:%M")
        text += (f"Список валют: <b>{oc.crypto_max_coins[user['crypto_max_coins']]}</b>\n"
                f"Премиум действует до <b>{premium_time}</b>\n")
    text += f"\nТакже можете <a href='https://t.me/obotov'>подписаться</a> на наш канал и узнавать первыми о новых нововедениях бота."
    return text


async def clbk_style(callback):
    await callback.answer("")
    await callback.message.edit_text(
        "Выбери стиль отображения валют."
        "\n1. Символы - более красивое отображение."
        "\n2. Названия - более информативное"
        "\nПример:"
        "\nUSD - $ (Символы)"
        "\nUSD - USD 🇺🇸 (Названия)",
        reply_markup=kb.set.change_style(),
    )
