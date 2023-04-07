from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardMarkup

# стартовое меню
start_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Блокнот'), KeyboardButton(text='Погода')],
    [KeyboardButton(text='Напоминалка'), KeyboardButton(text='AI')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите команду из меню')

# меню напоминалки
reminder_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить')],
    [KeyboardButton(text='Назад')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите команду из меню')

# кнопка для отправки геолоки
send_location = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Отправить геолокацию',
                    request_location=True),
     KeyboardButton(text='Назад')]],
    resize_keyboard=True,
    input_field_placeholder='Отправьте вашу геолокацию:')

add_record_button = InlineKeyboardButton('добавить',
                                         callback_data='add_record')

add_record = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('добавить', callback_data='add_record')]])

change_reminder_time = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Отложить на 15 минут',
                          callback_data='fifteen_minutes')],
    [InlineKeyboardButton('Отложить на 1 час',
                          callback_data='one_hour')],
    [InlineKeyboardButton('Подтвердить',
                          callback_data='reminder_done')]
])

# универсальная кнопка назад (в стартовое меню)
back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад')]],
                           resize_keyboard=True)
