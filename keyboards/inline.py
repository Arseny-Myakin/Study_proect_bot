from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicons.lexicons_ru import MAIN_MENU_BTNS_IN

async def inline_menu_kb():
    s=[]
    for text,data in MAIN_MENU_BTNS_IN.items():
        button = InlineKeyboardButton(
            text = text,
            callback_data = data
        )
        s.append([button])
    keyboards = InlineKeyboardMarkup(
        inline_keyboard = s,
        resize_keyboard = True
    )
    return keyboards