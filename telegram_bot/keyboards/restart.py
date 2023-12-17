from aiogram import types

def generate_restart_kb(common_ans: list[str]):
    restart = []
    for n, ans in enumerate(common_ans):
        restart.append([
            types.InlineKeyboardButton(text = ans[:60],
                                       callback_data = "generate_" + str(n))
            ])

    restart.append([
        types.InlineKeyboardButton(text="Вернуться в меню ⤴️",
                                   callback_data="return")
    ])
    print('___________________-------------------_____________', restart)
    restart_kb = types.InlineKeyboardMarkup(
        inline_keyboard=restart)
    
    return restart_kb


