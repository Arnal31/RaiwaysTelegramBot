import requests
import exceptions

from bs4 import BeautifulSoup
from lxml import html
from collections import Counter
from collections import namedtuple

comfortable_format = namedtuple('format',
                                'num, way, departure_time, departure_date, time, arrival_time, arrival_date, pricing')
text_url = namedtuple('format', 'text, url')


class RailParse:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9'
        }

    def get_page(self, departure, arrival, departure_date, arrival_date=''):

        url = f"https://bilet.railways.kz/sale/default/route/search" \
              f"?route_search_form%5BdepartureStation%5D={departure}" \
              f"&route_search_form%5BarrivalStation%5D={arrival}" \
              f"&route_search_form%5BforwardDepartureDate%5D={departure_date}" \
              f"%2C+%D1%81%D1%80%D0%B4&route_search_form%5BbackwardDepartureDate%5D={arrival_date}" \
              f"&_locale=ru" \

        r = self.session.get(url)
        return text_url(text=r.text, url=r.url)

    def price_and_type(self, item):
        train_type = item.select('table.ui.two.column.equal.width.very.basic.table.mobile.hidden tbody tr')

        all_types = []
        for train_types in train_type:
            train_types1 = train_types.select_one('td.left.aligned h4.ui.header').find(text=True,
                                                                                       recursive=False).strip()
            all_types.append(train_types1)

        all_price = []
        for train_prices in train_type:
            train_place = train_prices.select_one('td.left.aligned span.sub.header').find(text=True,
                                                                                          recursive=False).strip().replace(
                'орын', 'место')
            train_price = train_prices.select_one('td.right.aligned h4.ui.apple.header ') \
                .find(text=True, recursive=False).strip().replace(u'\xa0', ' ')
            all_price.append(train_price + train_place)

        type_price = {}
        for carriage_type, carriage_price in zip(all_types, all_price):
            type_price[carriage_type] = carriage_price

        return type_price

    def parse_method(self, item):
        # Номер поезда
        numb = item.select_one("h3.ui.header.mobile.hidden.train-information")
        numb = numb.get_text().strip().strip('Сипаттамасы').strip('Описание').strip()

        # Поезд
        way = item.select_one('h4.ui.header.mobile.hidden.train-route span.sub.header')
        way = way.get_text().strip().replace('  ', ' - ')

        # Время отправления
        departure_time = item.select_one('h2.ui.header.mobile.hidden.departure-time')
        departure_time = departure_time.find(text=True, recursive=False).strip()

        # Дата отправления
        departure_date = item.select_one('h2.ui.header.mobile.hidden.departure-time span.sub.header')
        departure_date = departure_date.string.strip()

        # Время в пути
        time = item.select_one('td.center.aligned.time-in-way h3.ui.header.mobile.hidden')
        time = time.text.strip()

        # Время прибытия
        arrival_time = item.select_one('h2.ui.header.mobile.hidden.arrival-time')
        arrival_time = arrival_time.find(text=True, recursive=False).strip()

        # Дата прибытия
        arrival_date = item.select_one('h2.ui.header.mobile.hidden.arrival-time span.sub.header')
        arrival_date = arrival_date.string.strip()

        # Тип вагона и цена
        pricing = self.price_and_type(item)

        return comfortable_format(
            num=numb,
            way=way,
            departure_time=departure_time,
            departure_date=departure_date,
            time=time,
            arrival_time=arrival_time,
            arrival_date=arrival_date,
            pricing=pricing
        )

    def get_block(self, departure, arrival, departure_date, arrival_date=''):
        text = self.get_page(departure=departure, arrival=arrival, departure_date=departure_date,
                             arrival_date=arrival_date)

        soup = BeautifulSoup(text.text, 'lxml')
        tr = soup.select("tr.train.item")
        if not tr:
            raise exceptions.NoTrainError
        train = []
        for item in tr:
            block = self.parse_method(item)
            train.append(block)
        return text_url(text=train, url=text.url)


rail_parse = RailParse()
