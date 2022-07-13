from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

GET_MOSCOW_CITIES = 'Обновить населенные пункты МО'


button_get_moscow_cities = KeyboardButton(GET_MOSCOW_CITIES)

start_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_buttons.add(button_get_moscow_cities)