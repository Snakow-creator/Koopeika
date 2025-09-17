from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest

from datetime import datetime
from loggers.logs import log

import commands.keyboards as kb
import database.requests as rq
import database.online_config as oc

router = Router()


# empty checkout
@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


# premium subscribe for month
async def payment_stars(callback: CallbackQuery, amount: int):
    price = oc.title_stars_price[amount]
    prices = [LabeledPrice(label="XTR", amount=price)]
    title = oc.title_stars.get(amount)
    await callback.message.answer_invoice(
        title="Koopeika Premium",
        description=f"{title} \n Покупая подписку, вы соглашаетесь с договором оферты в /info",
        prices=prices,
        payload=f"premium_subscribe_{amount}",
        provider_token=None,  # Telegram Stars
        currency="XTR",
        reply_markup=kb.pay.premium(amount=price),
    )


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    amount = payload.split("_")[-1]
    if payload.startswith("premium_subscribe_"):
        await give_premium_month(message, int(amount))


# successful payment for month
async def give_premium_month(message: Message, amount: int):
    premium_until = await rq.Edit.premium_extend(message.from_user.id, amount)
    premium_time = datetime.strftime(premium_until, "%d.%m.%Y %H:%M")
    transaction_id = message.successful_payment.telegram_payment_charge_id
    log.debug(f"Successful payment for {amount} {transaction_id}")
    title = oc.title_stars_for_db.get(amount)

    await rq.Payments.add(message.from_user.id, transaction_id, title)
    await message.answer(
        f"Оплата прошла успешно✅\n"
        f"Подписка продлена до <b>{premium_time}</b>\n"
        f"Спасибо за поддержку нашего бота✨\n"
        f"Рефаунд: <code>{transaction_id}</code>"
    )


@router.message(Command("refund"))
async def сmd_refund(message: Message, bot: Bot, command: CommandObject):
    if message.from_user.id == 1429466470:
        log.debug(f"Refund by admin {message.from_user.id}")
        transaction_id = command.args
        if not transaction_id:
            await message.answer("Неверно указан /refund АЙДИ")
            return
        try:
            user_obj = await rq.Payments.load(transaction_id)
            user_id = user_obj.user["tg_id"]
            await bot.refund_star_payment(user_id=user_id, telegram_payment_charge_id=transaction_id)
            await rq.Edit.premium_refund(user_id, transaction_id)
            await message.answer("Возврат произведен успешно✅")

        except AttributeError as error:
            await bot.refund_star_payment(
                user_id=message.from_user.id, telegram_payment_charge_id=transaction_id
            )
            log.debug(f"Refund to admin {message.from_user.id}")
            await message.answer("Рефаунд был вернут тестеру")
        except TelegramBadRequest as error:
            if "CHANGE NOT FOUND" in error.message:
                text = "Транзакция не была найдена"
                log.error(f"CHANGE NOT FOUND: Транзакция не была найдена {transaction_id}")

            elif "CHARGE_ALREADY_REFUNDED" in error.message:
                text = "За эту покупку уже был возврат средств"
                log.error(f"CHARGE_ALREADY_REFUNDED: За эту покупку уже был возврат средств {transaction_id}")

            else:
                text = "Транзакция не была найдена"
                log.error(f"{error.message}: Транзакция не была найдена {transaction_id}")

            await message.answer(text)
            return
