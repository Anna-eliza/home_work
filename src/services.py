from collections import Counter
import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Фильтрует операции по поисковой строке в описании."""
    if not search or not data:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [transaction for transaction in data if pattern.search(transaction.get("description", ""))]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество банковских операций по категориям."""
    if not categories:
        return {}

    unique_categories = list(dict.fromkeys(categories))

    counter = Counter()

    for transaction in data:
        description = transaction.get("description", "").lower()

        for category in unique_categories:
            if category.lower() in description:
                counter[category] += 1

    return {category: counter[category] for category in unique_categories}
