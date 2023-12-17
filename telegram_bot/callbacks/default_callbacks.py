from generate.search_and_gen import get_answer
from telegram_bot.keyboards.restart import generate_restart_kb
from telegram_bot.routers.default_routers import default_router as router
from telegram_bot.states.user_state import UserState
from aiogram import types
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.keyboards.menu import menu_kb



# Обработка похожих вопросов

@router.callback_query(F.data == "download_file", UserState.menu_state)
async def handle_download(callback : types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Отправьте файл для дообучения 📄")
    await state.set_state(UserState.download_state)
    await callback.answer()

@router.callback_query(F.data == "return")
async def handle_return(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.menu_state)
    await callback.message.answer(text="Привет 🖐️. Ты можешь помочь мне обучением, добавив свой файл, или я могу ответить на интересующий тебя вопрос", \
        reply_markup=menu_kb)
    await callback.answer()


@router.callback_query(F.data == "restart")
async def handle_new_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Задайте вопрос, я помогу на него ответить 🧐")
    await state.set_state(UserState.answer_state)
    await callback.answer()
  

@router.callback_query(F.data.startswith("generate_"), UserState.start_state)
async def handle_sim_question(callback: types.CallbackQuery, state: FSMContext):
    button_text = callback.data.replace('generate_', '')
    button_text = callback.message.reply_markup.inline_keyboard[int(button_text)][0].text
    print('*************************************', button_text)

    gen_msg = await callback.message.answer(
        "Подождите немного, я генерирую ответ... 🕐"
    )

    ans, r = get_answer(button_text)

    print(r)

    await state.set_state(UserState.start_state)

    await gen_msg.edit_text("Ответ: ")
    for i in range(len(ans)):
        await callback.message.answer(f"{ans[i]}")

    await callback.message.answer("Нажмите на кнопку, чтобы начать заново или вернуться в меню", reply_markup = generate_restart_kb(r))
    await callback.answer()
    

@router.callback_query(F.data == "ask_question")
async def handle_ask_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Задайте вопрос, я помогу на него ответить 🧐")
    await state.set_state(UserState.answer_state)
    await callback.answer()