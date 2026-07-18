from datetime import datetime

from aiogram.types import CallbackQuery, Message, LabeledPrice

from config import conf
from payments.request import Payments as payments_req
from settings import edit_req

from keyboards import pay
from tasks.logger import log




# premium subscribe for month
async def payment_stars(callback: CallbackQuery, amount: int):
    price = conf.title_stars_price[amount] # get price by amount
    prices = [LabeledPrice(label="XTR", amount=price)]
    title = conf.title_stars.get(amount) # get text by amount
    await callback.message.answer_invoice(
        title="Koopeika Premium",
        description=f"{title} \n Покупая подписку, вы соглашаетесь с договором оферты в /info",
        prices=prices,
        payload=f"premium_subscribe_{amount}",
        provider_token=None,  # Telegram Stars
        currency="XTR",
        reply_markup=pay.premium(amount=price),
    )


# successful payment for month
async def give_premium_month(message: Message, amount: int):
    premium_until = await edit_req.premium_extend(message.from_user.id, amount)
    premium_time = datetime.strftime(premium_until, "%d.%m.%Y %H:%M")
    transaction_id = message.successful_payment.telegram_payment_charge_id

    log.debug(f"Successful payment for {amount} {transaction_id}")
    title = conf.title_stars_for_db.get(amount) # get title by amount

    await payments_req.add(message.from_user.id, transaction_id, title)
    await message.answer(
        f"Оплата прошла успешно✅\n"
        f"Подписка продлена до <b>{premium_time}</b>\n"
        f"Спасибо за поддержку нашего бота✨\n"
        f"Рефаунд: <code>{transaction_id}</code>"
    )
