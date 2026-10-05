import json
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)

utils_file_handler = logging.FileHandler(
    LOGS_DIR / "utils.log",
    mode="w",
    encoding="utf-8",
)

utils_file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

utils_file_handler.setFormatter(utils_file_formatter)
utils_logger.addHandler(utils_file_handler)
utils_logger.propagate = False


def load_operations(path):
    """Загружает список транзакций из JSON-файла.

    Возвращает [] если файл не найден, пустой,
    или содержит не список.
    """

    utils_logger.debug("Попытка загрузки транзакций из файла: %s", path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:

        utils_logger.error("Файл не найден: %s", path)
        return []
    except json.JSONDecodeError as e:

        utils_logger.error("Ошибка декодирования JSON в файле %s: %s", path, e)
        return []

    if not isinstance(data, list):

        utils_logger.error(
            "Ожидался список транзакций в %s, получено: %s",
            path,
            type(data).__name__,
        )
        return []

    utils_logger.info("Успешно загружено %d транзакций из %s", len(data), path)
    return data

    if not isinstance(data, list):
        return []

    return data
