from keyboards.inline import inline_progmarks_kb, choice_marks_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from lexicons.lexicons_ru import MAIN_PROGMARKS_BTNS_IN, PROG_MARKS_TEXT, MENU_TEXT

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

@router.callback_query(F.data == "change")
async def add_marks(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(
        "Выберите оценку на которую вы исправите все двойки (только одно число)",
        reply_markup=await choice_marks_kb()
    )

@router.callback_query(F.data.startswith("choice"))
async def add_marks(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    marks = data.get("marks","")
    new_mark = callback.data.split("_")[-1]
    print(new_mark,marks,marks.replace("2",new_mark))
    new_text = marks.replace("2",new_mark)
    fake_message = callback.message.model_copy(update={"text": new_text})

    await process_marks(fake_message, state)








