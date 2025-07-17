import database.online_config as oc


async def choise_value(action, style=None, num=None):
    if action[0:2] == "⭐️":
        value = "⭐️"
    else:
        value = action
    answer_ = f"Вы выбрали: {oc.values[action]} ({value})"
    if style and num:
        text = f"Вы выбрали: <b>{num}{oc.values_symbols[style][action]}</b>"
    else:
        text = f"Вы выбрали: <b>{oc.values[action]}</b> (<b>{value}</b>)"
    return answer_, text
