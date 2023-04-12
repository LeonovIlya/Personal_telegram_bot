import datetime as dt

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from rutimeparser import parse, get_clear_text

import config
import keyboard

from reminder.db.db_ops import add_rec, get_recs, make_done_rec, \
    change_time, check_recs
from states import UserState

bot = Bot(token=config.BOT_TOKEN)

reminder_result = None


async def check_records():
    time_now = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    result = check_recs(time_now)
    if result is not None:
        await bot.send_message(chat_id=result.user_id,
                               text=f'НАПОМИНАНИЕ!\n'
                                    f'{result.reminder_time.strftime("%d/%m/%Y, %H:%M")}\n'
                                    f'{result.text}',
                               reply_markup=keyboard.change_reminder_time)
        global reminder_result
        reminder_result = result
    else:
        pass


async def set_add_record(message: types.Message):
    await message.answer(text='Введите запись:',
                         reply_markup=keyboard.back)
    await UserState.reminder_add.set()


async def add_record(message: types.Message):
    user_id = message.from_user.id
    datetime = parse(message.text)
    if datetime is not None:
        text = get_clear_text(message.text)
        add_rec(user_id, datetime, text)
        await message.answer(text='Запись успешно добавлена!',
                             reply_markup=keyboard.back)
    else:
        await message.answer(text='Время и/или дата не обнаружены, '
                                  'попробуйте еще раз!',
                             reply_markup=keyboard.back)


async def get_records(message: types.Message):
    text = get_recs(user_id=message.from_user.id)
    if text:
        await message.answer(text='\n'.join(' - '.join(i) for i in text),
                             reply_markup=keyboard.reminder_menu)
    else:
        await message.answer(text='Записей нет!',
                             reply_markup=keyboard.reminder_menu)
    await UserState.reminder.set()


async def change_reminder_time(callback: types.CallbackQuery):
    if callback.data == 'fifteen_minutes':
        new_time = reminder_result.reminder_time + dt.timedelta(minutes=15)
        change_time(rec_id=reminder_result.id, new_time=new_time)
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer(text='Напоминание отложено на 15 минут!',
                                      reply_markup=keyboard.back)
    elif callback.data == 'one_hour':
        new_time = reminder_result.reminder_time + dt.timedelta(hours=1)
        change_time(rec_id=reminder_result.id, new_time=new_time)
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer(text='Напоминание отложено на 1 час!',
                                      reply_markup=keyboard.back)
    elif callback.data == 'reminder_done':
        make_done_rec(rec_id=reminder_result.id)
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None)
        await callback.message.answer(text='Напоминание подтверждено!',
                                      reply_markup=keyboard.back)
    else:
        print('Something went wrong!')


def register_handlers_reminder(dp: Dispatcher):
    dp.register_message_handler(get_records,
                                text="Напоминалка",
                                state=UserState.auth)
    dp.register_message_handler(set_add_record,
                                text="Добавить",
                                state=UserState.reminder)
    dp.register_message_handler(add_record,
                                state=UserState.reminder_add)
    dp.register_callback_query_handler(change_reminder_time,
                                       state='*')
