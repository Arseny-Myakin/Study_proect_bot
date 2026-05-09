from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicons.lexicons_ru import MAIN_MENU_BTNS


async def menu_kb():
    """Создает reply клавиатуру из словаря MAIN_MENU_BTNS"""
    s=[]
    for text in MAIN_MENU_BTNS:
        button = KeyboardButton(
            text = text
        )
        s.append([button]) # каждая кнопка в отдельном ряду
    keyboards = ReplyKeyboardMarkup(
        keyboard = s,
        resize_keyboard = True # автоматически подгоняет размер кнопок
    )
    return keyboards