import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from bot.init_bot import engine
from db.models import Cities
from db.service import get_or_create
import logging


class WikiParse:

    def __init__(self):
        self.main_url = 'https://ru.wikipedia.org/wiki/Городские_населённые_пункты_Московской_области'
        self.data_list = []
        self.msg_error = 'Не удалось обновить данные, попробуйте позже.'
        self.msg_success = 'Данные успешно обновлены.'

    def get_data_from_wiki(self) -> str:
        response = requests.get(self.main_url)
        if response.status_code != 200:
            return self.msg_error
        try:
            self._parse_html(response)
            self._create_or_update_cities()
            return self.msg_success
        except Exception as e:
            logging.critical(f'Критичная ошибка: {e}')
            return self.msg_error

    def _parse_html(self, response: requests.Response) -> None:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', attrs={'class': 'standard sortable'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        logging.info(rows)
        for row in rows:
            link_and_title_column = row.select_one("td:nth-of-type(2)")  # 2 столбец таблицы
            population_column = row.select_one("td:nth-of-type(5)")  # 3 столбец таблицы
            if link_and_title_column and population_column:
                link_and_title = link_and_title_column.find('a')
                link = link_and_title['href']
                title = link_and_title['title']
                population = population_column['data-sort-value']
                self.data_list.append({
                    'title': title,
                    'link': link,
                    'population': population,
                })

    def _create_or_update_cities(self) -> None:
        session = Session(bind=engine)
        for data in self.data_list:
            elem, created = get_or_create(
                session=session,
                model=Cities,
                defaults={'link': data['link'], 'population': data['population']},
                title=data['title'],
            )
            if not created and (elem.link != data['link'] or elem.population != int(data['population'])):
                logging.info(f'Изменена ссылка с {elem.link} на {data["link"]}')
                logging.info(f'Изменена популяция с {elem.population} на {data["population"]}')
                elem.link = data['link']
                elem.population = data['population']
                session.add(elem)
        session.commit()
