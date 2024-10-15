import requests
import json
import telebot
from T_K import keys


class APIException(Exception):
    pass


class API:
    @staticmethod
    def get_price(base, quote, amount):
        if quote == base:
            raise APIException(f'Невозможно перевести 2 одинаковые валюты {base}!')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать сумму {amount}')

        quote_ticker, base_ticker = keys[quote], keys[base]

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

    @staticmethod
    def get_values():
        text = 'Доступные валюты:'
        for key in keys:
            text = "\n".join((text, key))
        return text