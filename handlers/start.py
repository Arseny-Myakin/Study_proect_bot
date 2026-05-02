from keyboards.reply import menu_kb
from keyboards.inline import inline_menu_kb
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from lexicons.lexicons_ru import START_TEXT, ADD_MARKS_TEXT

router = Router()


@router.message(Command(commands = ['start']))
async def start_handler(message:Message):
    await message.answer(START_TEXT, reply_markup= await inline_menu_kb())