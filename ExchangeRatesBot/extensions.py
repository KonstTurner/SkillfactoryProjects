import json
import requests
from config import currency


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, symbols, amount):
        try:
            base_key = currency[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            symbols_key = currency[symbols.lower()]
        except KeyError:
            raise APIException(f"Валюта {symbols} не найдена!")

        if base_key == symbols_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        payload = {}
        headers = {"apikey": "Us1g3rPQxzSRym3CWrJa4n3nWtVADQfZ"}

        r = requests.request("GET", f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols_key}&base={base_key}", headers=headers, data = payload)
        resp = json.loads(r.content)
        new_price = resp["rates"][symbols_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {symbols} : {new_price}"
        return message




