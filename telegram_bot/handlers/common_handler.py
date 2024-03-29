from aiogram import types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
import os
from telegram_bot.states.user_state import UserState
from telegram_bot.routers.default_routers import default_router as router
from telegram_bot.keyboards.restart import generate_restart_kb
from telegram_bot.keyboards.menu import menu_kb
from telegram_bot.keyboards.get_back import return_kb
import telegram_bot.callbacks.default_callbacks
from generate.search_and_gen import get_answer
from generate import vectordb
from db_utils.db_func import add_file_to_db

# Обработка команды старта бота

@router.message(Command("start"))
async def start_bot(msg: Message, state: FSMContext):
    await state.set_state(UserState.menu_state)
    await msg.answer(text="Привет 🖐️. Ты можешь помочь мне с обучением, добавив свой файл, или я могу ответить на интересующий тебя вопрос", \
        reply_markup=menu_kb)
    


# отрисовка меню     

@router.message(UserState.menu_state)
async def handle_menu(msg: Message, state: FSMContext):
    await state.set_state(UserState.menu_state)
    await msg.answer(text="Добавь файлы или задай мне интересный вопрос 👉🏻👈🏻", \
        reply_markup=menu_kb)



# Переход из состояния старта в состояние ввода пользователем команды

@router.message(UserState.start_state)
async def handle_start_button(msg: Message, state: FSMContext):
    await msg.answer(text="Задайте вопрос, я помогу на него ответить 🧐")
    await state.set_state(UserState.answer_state)

    
# Отправка ответа на запрос пользователя

@router.message(UserState.answer_state, F.text)
async def generate_answer(msg: Message, state: FSMContext):
    
    gen_msg = await msg.answer(
        "Подождите немного, я генерирую ответ... 🕐"
    )
    
    ans, r = get_answer(msg.text)

    print(r)

    await state.set_state(UserState.start_state)
    
    
    
    await gen_msg.edit_text("Ответ: ")
    for i in range(len(ans)):
        await msg.answer(f"{ans[i]}")
    
    await msg.answer("Нажмите на кнопку, чтобы начать заново или вернуться в меню", reply_markup=generate_restart_kb(r))



# Обработка отправки файла

@router.message(UserState.download_state, F.document)
async def handle_file(msg: Message, state: FSMContext):
    file_id_doc = msg.document.file_id
    file = await msg.bot.get_file(file_id_doc)
    file_path = file.file_path

    local_path = f"./data/{msg.document.file_name}"



    if os.path.exists(local_path) == False:
        await msg.bot.download_file(file_path, local_path)

        add_file_to_db(vectordb, local_path)

        await msg.answer("Добавила, вернитесь в меню или продолжайте... 👉🏻👈🏻", reply_markup=return_kb)
    else:
        await msg.answer("Упс, такой файл уже существует, попробуйте добавить другой файл",
                         reply_markup=return_kb)
    