"""Обработчик авторизации пользователя"""

from aiogram import types, Dispatcher

import config
import keyboard
from states import UserState
from notebook.notebook import create_file


# проверяем разрешение на доступ к боту
async def auth_user(message: types.Message):
    if str(message.from_user.id) in config.ID_AUTH_USERS:
        await message.answer(text='Поздравляю! У вас есть доступ к боту!\n')
        await create_file(user_id=message.from_user.id)
        await start_menu(message)
        await UserState.auth.set()
    else:
        await message.answer(text='У вас нет доступа к боту!')


# стартовое меню бота
async def start_menu(message: types.Message):
    await message.answer(text='Выберите команду:',
                         reply_markup=keyboard.start_menu)
    await UserState.auth.set()


# компануем в обработчик
def register_handlers_auth(dp: Dispatcher):
    dp.register_message_handler(auth_user)
    dp.register_message_handler(start_menu, text="Назад", state='*')
