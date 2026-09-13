Operation = dict[str, str | int]


def filter_by_state(
    list_dicts: list[Operation],
    state: str = "EXECUTED",
) -> list[Operation]:
    """Фильтрует список словарей по значению ключа 'state'."""
    filtered_list = []
    for item in list_dicts:
        if item.get("state") == state:
            filtered_list.append(item)
    return filtered_list


def sort_by_date(
    operations: list[Operation],
    reverse: bool = True,
) -> list[Operation]:
    """Сортирует список словарей по дате."""
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)
