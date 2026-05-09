from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from lexicons.lexicons_ru import MENU_TEXT_OUR,MENU_TEXT0, DEL_MARKS_TXT,ADD_MARKS_TEXT,DEL_MARKS_TXT_K,DEL_MARKS_TXT_K1,ADD_MARKS_TEXT1, DEL_MARKS_TXT_RES
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
    await state.update_data({"marks":message.text})
    #await state.update_data(marks = data.get('marks','') + message.text)

    list_marks = list(map(int, list(message.text)))
    del_marks = sum(list_marks) / len(list_marks) # рассчет среднего балла
    add_sr = float(data.get('sr_add'))
    k = len(list_marks) * (add_sr - del_marks) / (5-add_sr) # формула для подсчета недостоющихся пятерок до желаемого балла

    await message.answer(f"{DEL_MARKS_TXT_RES}  {str(round(del_marks,2))} \n {DEL_MARKS_TXT_K(add_sr)}  {str(ceil(k))}  {DEL_MARKS_TXT_K1}")
    print("[LOG] Вывел результат")
    await state.clear() # очищает данные состояния



