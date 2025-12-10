from config import conf


#action[:3] -> cryptovalues
async def choise_value(action, style=None, num=None):
    if action[0:2] == "⭐️":
        value = "⭐️"
    else:
        value = action
    answer = f"Вы выбрали: {conf.values.get(action, action)} ({value})"
    if style and num:
        text = f"Вы выбрали: <b>{num}{conf.values_symbols[style].get(action, action)}</b>"
    else:
        text = f"Вы выбрали: <b>{conf.values.get(action, action)}</b> (<b>{value}</b>)"
    return answer, text
