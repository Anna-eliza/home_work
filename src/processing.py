def filter_by_state(list_dicts: list[dict[str, str | int]], state: str = 'EXECUTED') -> list[dict[str, str | int]]:
    """Фильтрует список словарей по значению ключа 'state'"""
    filtered_list = []
    for item in list_dicts:
        if item.get('state') == state:
            filtered_list.append(item)
    return filtered_list
