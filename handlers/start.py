from keyboards.inline import inline_menu_kb
from keyboards.reply import menu_kb
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from lexicons.lexicons_ru import START_TEXT, START_TEXT_1

router = Router()


@router.message(Command(commands = ['start']))
async def start_handler(message:Message):
    """"Эта функция отвечает на команду start"""
    print("[LOG] Старт запущен")
    await message.answer(START_TEXT, reply_markup= await menu_kb())
    await message.answer(START_TEXT_1, reply_markup= await inline_menu_kb())