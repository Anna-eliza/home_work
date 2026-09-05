from typing import Dict, List


def filter_by_state(list_dicts: list[dict[str, str | int]], state: str = "EXECUTED") -> list[dict[str, str | int]]:
    """Фильтрует список словарей по значению ключа 'state'"""
    filtered_list = []
    for item in list_dicts:
        if item.get("state") == state:
            filtered_list.append(item)
    return filtered_list


def sort_by_date(operations: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """Сортирует список словарей по дате"""
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)
