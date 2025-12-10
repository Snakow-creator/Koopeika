from keyboards.assets import AssetsKeyboard
from keyboards.settings import SettingsKeyboard
from keyboards.conversion import ConversionKeyboard
from keyboards.payment import PaymentKeyboard
from keyboards.transactions import TransactionsKeyboard

from keyboards.info import info_regions, back_info_regions

from base.keyboard import main_menu
from keyboards.balance import dinamic_assets, back_to_balance


# tx - transaction
# kb - keyboard
# seg - settings
# con - conversion

# objects which have methods keyboards
seg = SettingsKeyboard
con = ConversionKeyboard
assets = AssetsKeyboard
pay = PaymentKeyboard
trx = TransactionsKeyboard

# functions and simple keyboards
