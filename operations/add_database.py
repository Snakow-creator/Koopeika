import database.online_config as oc


async def check_list_values(action, style=None, num=None):
    value = action
    answer_ = f"Вы выбрали: {oc.values[action]} ({value})"
    if style and num:
        text = f"Вы выбрали: <b>{num}{oc.values_symbols[style][action]}</b>"
    else:
        text = f"Вы выбрали: <b>{oc.values[action]}</b> (<b>{value}</b>)"
    return value, answer_, text
