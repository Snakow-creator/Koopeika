import os

from dotenv import load_dotenv
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties

static_cryptolist = ["BTC", "ETH", "SOL", "TON"]
dinamic_cryptolist = []
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML)
DEBUG = False  # change to True for debug


NBK_API: str = os.getenv("NBK_API")
CRYPTO_API: str = os.getenv("CRYPTO_API")
CRYPTO_TOP_API: str = os.getenv("CRYPTO_TOP_API")
