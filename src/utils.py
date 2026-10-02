import json


def load_operations(path):
    """Загружает список транзакций из JSON-файла.

    Возвращает [] если файл не найден, пустой,
    или содержит не список.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return data
