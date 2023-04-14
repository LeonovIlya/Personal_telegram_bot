"""Обработчик модуля записной книжки"""

import os

from aiogram import types, Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext

import keyboard
from states import UserState
from notebook.notebook import read_file, write_file, delete_record
from notebook.voice_recognition import STT

stt = STT()

# словарь соответствия чисел
numbers_dict = {'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5,
                'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9,
                'десять': 10, 'одиннадцать': 11., 'двенадцать': 12,
                'тринадцать': 13, 'четырнадцать': 14, 'пятнадцать': 15,
                'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18,
                'девятнадцать': 19, 'двадцать': 20}

# список слов удаления
delete_words = ['удалить', 'удали', 'удалит', 'залить', 'долить', 'вдали']


# получаем голосовое сообщение и распознаём, если первое слово удалить
# и второе цифра из словаря - удаляем запись
async def get_voice(message: types.Message, state: FSMContext):
    if isinstance(message.content_type, type(types.ContentType.VOICE)):
        if voice_file := message.voice:
            await voice_file.download(
                destination_file='./notebook/voice_file.ogg')
        text = stt.audio_to_text(audio_file='./notebook/voice_file.ogg')
        if text:
            if text.split()[0] in delete_words \
                    and text.split()[1] in numbers_dict.keys():
                await delete_record(user_id=message.from_user.id,
                                    text=numbers_dict[text.split()[1]])
                await get_records(message)
            else:
                await message.answer(text, reply_markup=keyboard.add_record)
                await state.update_data(text_to_add=text)
                os.remove('./notebook/voice_file.ogg')
        else:
            await message.answer(text='Непонятно, давай еще раз!',
                                 reply_markup=keyboard.back)
    else:
        await message.answer(text='Это не голосовуха! Попробуй еще раз!',
                             reply_markup=keyboard.back)


# добавляем запись если нажата инлайн-кнопка добавить
async def add_record(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await write_file(user_id=callback.from_user.id, text=data['text_to_add'])
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    await callback.message.answer(text='Запись добавлена!',
                                  reply_markup=keyboard.back)
    await get_records(callback.message)


# получаем все записи блокнота
async def get_records(message: types.Message):
    text = await read_file(user_id=message.chat.id)
    if text:
        await message.answer(text=text,
                             reply_markup=keyboard.back)
        await UserState.voice.set()
    else:
        await message.answer(text='Записей нет!',
                             reply_markup=keyboard.back)
        await UserState.voice.set()


# компануем в обработчик
def register_handlers_notebook(dp: Dispatcher):
    dp.register_message_handler(get_records,
                                text="Блокнот",
                                state=UserState.auth)
    dp.register_message_handler(get_voice,
                                content_types=[ContentType.VOICE],
                                state=UserState.voice)
    dp.register_callback_query_handler(add_record,
                                       state=UserState.voice)
