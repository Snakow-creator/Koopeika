import database.online_config as oc


#action[:3] -> cryptovalues
async def choise_value(action, style=None, num=None):
    if action[0:2] == "⭐️":
        value = "⭐️"
    else:
        value = action
    answer = f"Вы выбрали: {oc.values.get(action, action)} ({value})"
    if style and num:
        text = f"Вы выбрали: <b>{num}{oc.values_symbols[style].get(action, action)}</b>"
    else:
        text = f"Вы выбрали: <b>{oc.values.get(action, action)}</b> (<b>{value}</b>)"
    return answer, text
