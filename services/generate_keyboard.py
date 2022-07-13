from aiogram import types
from sqlalchemy.orm import Session

from bot.init_bot import engine
from db.models import Cities
from functools import lru_cache


@lru_cache
def generate_inline_keyboard(city_name: str) -> types.InlineKeyboardMarkup:
    session = Session(bind=engine)
    cities = session.query(Cities).filter(Cities.title.ilike(f'{city_name}%')).all()
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for city in cities:
        btn_text = city.title
        callback_data = city.id
        keyboard.add(types.InlineKeyboardButton(text=btn_text, callback_data=callback_data))
    return keyboard
