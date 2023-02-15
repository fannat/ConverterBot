import requests
import json
from Config import val


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты ')

        try:
            quote_mask = val[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_mask = val[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'''Не удалось обработать количество {amount}.\nИспользуйте только цифры и при\
        необходимости точку в качестве десятичного разделителя,нажмите \help для инструкций''')

        resp = requests.get(
            f"https://api.apilayer.com/currency_data/convert?to={base_mask}&from={quote_mask}&amount={amount}",
            headers={"apikey": "INf3W4C47Lrp5Q3eO8vb86j67a3zEZVu"})
        rate = json.loads(resp.content)['result']

        return rate



