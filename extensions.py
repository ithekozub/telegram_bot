import requests
import json
from config import symbols, API_KEY


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_tiker = symbols[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту{quote}')

        try:
            base_ticker = symbols[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту{base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        req_part = f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}'

        if base_ticker == 'EUR':
            r = requests.get(f'{req_part}&symbols={quote_tiker}')
            total_base = float(json.loads(r.content)['rates'][quote_tiker]) * amount
        else:
            r_q = requests.get(f'{req_part}&symbols={quote_tiker}')
            r_b = requests.get(f'{req_part}&symbols={base_ticker}')
            price_q = float(json.loads(r_q.content)['rates'][quote_tiker])
            price_b = float(json.loads(r_b.content)['rates'][base_ticker])
            total_base = (price_b / price_q) * amount

        return round(total_base, 3)
