from aiogram import types, Dispatcher

import keyboard
from ai.ai import get_response
from auth.handler import start_menu
from states import UserState


# Спрашиваем вопрос для ИИ
async def set_ai_state(message: types.Message):
    await message.answer(text='Напишите ваш запрос ИИ:',
                         reply_markup=types.ReplyKeyboardRemove())
    await UserState.ai.set()


# Получаем вопрос, отправляем ИИ, получаем ответ ИИ, выводим ответ в чат
async def get_answers(message: types.Message):
    text = await get_response(message.text)
    await message.answer(text=text,
                         reply_markup=keyboard.back)


# компануем в обработчик
def register_handlers_ai(dp: Dispatcher):
    dp.register_message_handler(set_ai_state,
                                text='AI',
                                state=UserState.auth)
    dp.register_message_handler(start_menu,
                                text='Назад',
                                state=UserState.ai)
    dp.register_message_handler(get_answers,
                                state=UserState.ai)
