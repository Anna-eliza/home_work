import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует список банковских операций по поисковой строке
    в описании.
    """
    if not search or not data:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [
        transaction for transaction in data
        if pattern.search(transaction.get('description', ''))
    ]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Подсчитывает количество банковских операций по каждой категории
    на основе поля description.
    """
    if not categories:
        return {}

    counter = Counter()

    for transaction in data:
        description = transaction.get('description', '')

        for category in categories:
            if category in description:
                counter[category] += 1

    return {category: counter[category] for category in categories}