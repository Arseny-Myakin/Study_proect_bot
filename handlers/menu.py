from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router,F
from aiogram.types import Message, CallbackQuery

from keyboards.inline import change_marks_kb, choice_marks_kb
from lexicons.lexicons_ru import MENU_TEXT_OUR,MENU_TEXT0, PROG_MARKS_TEXT,ADD_MARKS_TEXT,DEL_MARKS_TXT_K,DEL_MARKS_TXT_K1,ADD_MARKS_TEXT1, DEL_MARKS_TXT_RES
from math import ceil

router = Router()

class MarksStates(StatesGroup): # определение класса состояния
    add_marks_state = State()
    sr_add_marks_state = State()

@router.message(F.text == MENU_TEXT0)
async def menu_handler(message: Message):
    """"Эта функция отвечает при нажатии на inline кнопку о нас"""
    print("[LOG] О нас запущен")
    await message.answer(MENU_TEXT_OUR)

@router.callback_query(F.data == "addmarks")
async def add_marks(callback: CallbackQuery, state: FSMContext):
    """"Эта функция обрабатывает нажатие кнопки"""
    print("[LOG] Пользователь нажал Добавьте оценки")
    await callback.message.answer(ADD_MARKS_TEXT)
    await state.set_state(MarksStates.sr_add_marks_state)

@router.message(MarksStates.sr_add_marks_state)
async def add_marks_handler(message: Message, state: FSMContext):
    """"Эта функция обрабатывает нажатие кнопки и ввод оценок пользователем"""
    print("[LOG] Добавьте оценки запущен")
    await state.update_data(sr_add = message.text)
    await message.answer(ADD_MARKS_TEXT1)
    await state.set_state(MarksStates.add_marks_state)

@router.message(MarksStates.add_marks_state)
async def process_marks(message: Message, state: FSMContext):
    """"Эта функция считатет средний балл и количество недостоющихся пятерок до желаемого балла"""
    print("[LOG] Считает средний балл и количество недостоющихся пятерок до желаемого балла")
    data = await state.get_data()
    await state.update_data(marks = message.text)
    #await state.update_data(marks = data.get('marks','') + message.text)

    list_marks = list(map(int, list(message.text)))
    del_marks = sum(list_marks) / len(list_marks) # рассчет среднего балла
    add_sr = float(data.get('sr_add'))

    k = len(list_marks) * (add_sr - del_marks) / ((5-add_sr) if add_sr < 5 else 1) # формула для подсчета недостоющихся пятерок до желаемого балла
    kb = await change_marks_kb()
    await message.answer(
        f"{DEL_MARKS_TXT_RES}  {str(round(del_marks,2))} \n {DEL_MARKS_TXT_K(add_sr)}  {str(ceil(k))}  {DEL_MARKS_TXT_K1}",
        reply_markup=kb
    )
    print("[LOG] Вывел результат")
    await state.set_state(None) # очищает данные состояния


@router.callback_query(F.data == "change")
async def add_marks(callback: CallbackQuery, state: FSMContext):
    """Эта функция показывает кнопки для выбора оценок"""
    print("[LOG] Пользователь выбирает оценки")
    await callback.message.answer(
        PROG_MARKS_TEXT,
        reply_markup=await choice_marks_kb()
    )

@router.callback_query(F.data.startswith("choice"))
async def add_marks(callback: CallbackQuery, state: FSMContext):
    """Эта функция позволяет выбрать оценку кнопкой вместо ручного ввода, подставляя её вместо двойки"""
    print("[LOG] Бот исправляет двойки")
    data = await state.get_data()
    marks = data.get("marks","")
    new_mark = callback.data.split("_")[-1]
    print(new_mark,marks,marks.replace("2",new_mark))
    new_text = marks.replace("2",new_mark)
    fake_message = callback.message.model_copy(update={"text": new_text})

    await process_marks(fake_message, state)

