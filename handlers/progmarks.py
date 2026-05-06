from keyboards.inline import inline_progmarks_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from lexicons.lexicons_ru import MAIN_PROGMARKS_BTNS_IN, PROG_MARKS_TEXT

router = Router()

class AddMarksStates(StatesGroup):
    progmarks = State()

@router.message(F.text == MENU_TEXT)
async def menu_adder(message: Message):
    await message.answer(
        "Вот inline меню",
        reply_markup = await inline_progmarks_kb()
    )

@router.callback_query(F.data == "progmarks")
async def progmarks(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(MAIN_PROGMARKS_BTNS_IN)
    await state.set_state(AddMarksStates.progmarks)

@router.message(AddMarksStates.progmarks)
async def progmarks_handler(message: Message, state: FSMContext):
    await state.update_data(progmarks=message.text)
    await message.answer(PROG_MARKS_TEXT)
    await state.set_state(AddMarksStates.progmarks)

@router.message(AddMarksStates.progmarks)
async def progress_marks(message: Message, state: FSMContext):
    data = await state.get_data()








