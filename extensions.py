import requests
import json
from config import keys

class APIException(Exception):
    pass

class Exchanger:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты "{base}"')
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта "{quote}" не найдена')
        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Валюта "{base}" не найдена')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]] * amount
        total_base = round(total_base, 3)
        return total_base
