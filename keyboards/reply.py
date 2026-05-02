from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicons.lexicons_ru import MAIN_MENU_BTNS


async def menu_kb():
    s=[]
    for text in MAIN_MENU_BTNS:
        button = KeyboardButton(
            text = text
        )
        s.append([button])
    keyboards = ReplyKeyboardMarkup(
        keyboard = s,
        resize_keyboard = True
    )
    return keyboards