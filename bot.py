from aiogram import Dispatcher
from aiogram.utils import executor

from bot.init_bot import dp
from bot.handlers import send_welcome, send_help, \
    send_info_about_update_cities, get_list_cities_from_db, get_info_about_city_callback


async def shutdown(dispatcher: Dispatcher) -> None:
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)