def filter_by_currency(transactions, currency):
    """Фильтрует транзакции по заданной валюте."""
    return (
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency
    )


def transaction_descriptions(transactions):
    """Генератор, который поочерёдно возвращает описание каждой транзакции."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start, end):
    """Генератор номеров банковских карт в формате 'XXXX XXXX XXXX XXXX'."""
    for number in range(start, end + 1):
        card = f"{number:016d}"
        yield f"{card[:4]} {card[4:8]} {card[8:12]} {card[12:]}"
