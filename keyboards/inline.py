from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicons.lexicons_ru import MAIN_MENU_BTNS_IN, MAIN_PROGMARKS_BTNS_IN, PROG_MARKS_BTN_IN_DICT

async def inline_menu_kb():
    """Создает inline клавиатуру из словаря MAIN_MENU_BTNS_IN"""
    s=[]
    for text,data in MAIN_MENU_BTNS_IN.items():
        button = InlineKeyboardButton(
            text = text,
            callback_data = data
        )
        s.append([button]) # каждая кнопка в отдельном ряду
    keyboards = InlineKeyboardMarkup(
        inline_keyboard = s
    )
    return keyboards


async def change_marks_kb():
    """Создает inline клавиатуру из словаря MAIN_PROGMARKS_BTNS_IN"""
    a = []
    for text,data in MAIN_PROGMARKS_BTNS_IN.items():
        button = InlineKeyboardButton(
            text = text,
            callback_data = data
        )
        a.append([button]) # каждая кнопка в отдельном ряду

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=a
    )
    return keyboards


async def choice_marks_kb():
    """Создает inline клавиатуру из словаря PROG_MARKS_BTN_IN_DICT"""
    data = PROG_MARKS_BTN_IN_DICT
    s = []
    for key, value in data.items():
        button = InlineKeyboardButton(
            text=key,
            callback_data=value
        )
        s.append([button]) # каждая кнопка в отдельном ряду

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=s,
        resize_keyboard=True
    )
    return keyboards