from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicons.lexicons_ru import MAIN_MENU_BTNS_IN, MAIN_PROGMARKS_BTNS_IN

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



async def inline_progmarks_kb():
    s = []
    for text, data in MAIN_PROGMARKS_BTNS_IN.items():
        button = InlineKeyboardButton(
            text=text,
            callback_data=data
        )
        s.append([button])
    keyboards = InlineKeyboardMarkup(
        inline_keyboard=s,
        resize_keyboard=True
    )
    return keyboards

async def change_marks_kb():

    button = InlineKeyboardButton(
        text="исправить оценки",
        callback_data="change"
    )

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboards


async def choice_marks_kb():
    data = {
        "3":"choice_3",
        "4":"choice_4",
        "5":"choice_5"
    }
    s = []
    for key, value in data.items():
        button = InlineKeyboardButton(
            text=key,
            callback_data=value
        )
        s.append([button])

    keyboards = InlineKeyboardMarkup(
        inline_keyboard=s,
        resize_keyboard=True
    )
    return keyboards