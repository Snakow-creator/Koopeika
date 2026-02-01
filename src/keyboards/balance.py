from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


dinamic_assets = InlineKeyboardMarkup(inline_keyboard=[
  [
    InlineKeyboardButton(text="Доли активовℹ️", callback_data="balance_dinamic_assets")
  ],
  [
    InlineKeyboardButton(text="Назад⬅️", callback_data="menu")
  ],
])

back_to_balance = InlineKeyboardMarkup(inline_keyboard=[
  [
    InlineKeyboardButton(text="Назад⬅️", callback_data="main_balance")
  ]
])
