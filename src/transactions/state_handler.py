from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import transaction_state
from core.exceptions import BadUserIdError, BadMessageText, BigNumError
from users import user_req
from transactions import transaction_req
from config import profile

from utils import checker_num, checker_id
from tasks.logger import log
from base.keyboard import main_menu


router = Router()


# operations with Transaction
@router.message(transaction_state.edit)
async def transaction_edit(message: Message, state: FSMContext):
    try:
        # get data
        prof = profile.get(message.from_user.id)
        user_obj = await user_req.load(message.from_user.id)
        # get user data
        premium_user = await user_obj.premium()
        user = user_obj.user
        # get transaction data
        tr_id = prof.tr_message_id # get transaction id
        transaction = await transaction_req.load(message.from_user.id)

        # check data
        await checker_num(message.text, user["value"], premium_user)

        # edit transaction
        amount = int(message.text)

        await transaction.edit(value=amount, num_id=tr_id)
        await message.answer("Транзакция успешно изменена!", reply_markup=main_menu)
        log.debug(f"Edit transaction {message.from_user.id}")

    except BadMessageText as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)
    except BigNumError as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)
    finally:
        await state.clear()
