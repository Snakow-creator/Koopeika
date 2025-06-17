import os

from dotenv import load_dotenv
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties

cryptolist = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "TONUSDT"]
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML)
DEBUG = False


NBK_API = os.getenv("NBK_API")
BINANCE_API: str = os.getenv("BINANCE_API")
