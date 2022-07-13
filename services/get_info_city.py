from sqlalchemy.orm import Session

from bot.init_bot import engine
from db.models import Cities
from functools import lru_cache


@lru_cache
def get_info_about_city(city_id: int) -> dict:
    session = Session(bind=engine)
    city = session.query(Cities).get(city_id)
    start_url = 'https://ru.wikipedia.org'
    answer = {
        'title': city.title,
        'link': start_url + city.link,
        'population': city.population,
    }
    return answer
