from aiogram import Router, F, Bot
from aiogram.types import Message, PreCheckoutQuery
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest

from settings import edit_req
from payments.request import Payments as payment_req
from tasks.logger import log

from keyboards import seg
from payments.payment import give_premium_month


router = Router(name="payments")

@router.message(Command("give_premium"))
async def give_premium(message: Message, command: CommandObject):
    if message.from_user.id == 1429466470:
        user_id = int(command.args)
        log.debug(f"Give premium to {user_id}")
        await edit_req.premium_extend(user_id)
        await message.answer(f"Вы дали премиум на месяц пользователю: <b><code>{user_id}</code></b>")


# empty checkout
@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    amount = payload.split("_")[-1]
    if payload.startswith("premium_subscribe_"):
        await give_premium_month(message, int(amount))


@router.message(Command("refund"))
async def сmd_refund(message: Message, bot: Bot, command: CommandObject):
    if message.from_user.id == 1429466470:
        log.debug(f"Refund by admin {message.from_user.id}")
        transaction_id = command.args
        if not transaction_id:
            await message.answer("Неверно указан /refund АЙДИ")
            return
        try:
            user_obj = await payment_req.load(transaction_id)
            user_id = user_obj.user["tg_id"]
            await bot.refund_star_payment(user_id=user_id, telegram_payment_charge_id=transaction_id)
            await edit_req.premium_refund(user_id, transaction_id)
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

            await message.answer(text, reply_markup=seg.main_menu())
            return
