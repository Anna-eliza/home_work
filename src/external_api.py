import os

from dotenv import load_dotenv
import requests

load_dotenv()


def convert_to_rub(transaction):
    """
    Принимает транзакцию (словарь) и возвращает сумму в рублях (float).
    Для RUB возвращает исходную сумму.
    Для USD/EUR конвертирует через внешний API.
    """
    amount = float(transaction["amount"])
    currency = transaction["currency"]

    if currency == "RUB":
        return amount

    # Для USD или EUR
    api_key = os.getenv("EXCHANGERATES_API_KEY")
    if not api_key:
        raise ValueError("API key not found")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params = {"from": currency, "to": "RUB", "amount": amount}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Проверка на HTTP-ошибки

    data = response.json()
    return float(data["result"])
