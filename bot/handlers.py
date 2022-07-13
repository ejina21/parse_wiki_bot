from aiogram import types
from aiogram.dispatcher import filters
from aiogram import md
from bot.buttons import start_buttons, GET_MOSCOW_CITIES
from bot.init_bot import dp, bot
from services.generate_keyboard import generate_inline_keyboard
from services.get_info_city import get_info_about_city
from services.parse_wki import WikiParse


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(msg: types.Message) -> None:
    await msg.answer(
        f'Приветствую, {msg.from_user.first_name}! Ты можешь обновить '
        'информацию о городах Московской области по кнопке ниже '
        'и получить информацию о каждом, написав мне его название и нажав на предложенный город.',
        reply_markup=start_buttons,
    )


@dp.message_handler(state='*', commands=['help'])
async def send_help(msg: types.Message) -> None:
    await msg.answer(
        f'{msg.from_user.first_name}, бот умеет собирать информацию о городах Московской области, '
        'выводить их название, численность населения и ссылку на описание города в википедии. '
        'Для получения информации о городе оправьте мне название города, либо начало названия '
        'и выберите из предложенного списка необходимый город.\nЕсли '
        'бот не может найти город, попробуйте обновить информацию, нажав на кнопку "Обновить населенные пункты МО".',
        reply_markup=start_buttons,
    )


@dp.message_handler(filters.Text(equals=GET_MOSCOW_CITIES), state='*')
async def send_info_about_update_cities(msg: types.Message) -> None:
    message = WikiParse().get_data_from_wiki()
    await msg.answer(message, reply_markup=start_buttons)


@dp.message_handler(state='*')
async def get_list_cities_from_db(msg: types.Message) -> None:
    keyboard = generate_inline_keyboard(msg.text)
    if keyboard['inline_keyboard']:
        await msg.answer('Выберите необходимый город:', reply_markup=keyboard)
    else:
        await msg.answer('Города с таким названием нет в Московской области=(')


@dp.callback_query_handler(lambda c: c.data, state='*')
async def get_info_about_city_callback(callback_query: types.CallbackQuery) -> None:
    code = callback_query.data
    city = get_info_about_city(code)
    await bot.send_message(
        callback_query.from_user.id,
        md.hlink(city['title'], city['link']) + md.text(f'\nНаселение: {city["population"]} человек'),
        parse_mode=types.ParseMode.HTML
    )