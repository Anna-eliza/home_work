import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)

masks_file_handler = logging.FileHandler(
    LOGS_DIR / "masks.log",
    mode="w",
    encoding="utf-8",
)

masks_file_formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

masks_file_handler.setFormatter(masks_file_formatter)
masks_logger.addHandler(masks_file_handler)
masks_logger.propagate = False


def get_mask_card_number(card_number: str | int) -> str:
    """Функция маскирует номер карты клиента"""

    masks_logger.debug("Вызов get_mask_card_number: %s", card_number)

    card_str = str(card_number).replace(" ", "")

    if card_str and not card_str.isdigit():
        masks_logger.error("Номер карты содержит нецифровые символы: %s", card_number)
        raise ValueError("Номер карты должен содержать только цифры")

    card_str = card_str[-16:]
    first_six = card_str[:6]
    last_four = card_str[-4:]
    masked = f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"

    masks_logger.info("Номер карты успешно замаскирован: %s", masked)
    return masked


def get_mask_account(account_number: str | int) -> str:
    """Функция маскирует номер банковского счета"""

    masks_logger.debug("Вызов get_mask_account: %s", account_number)

    account_str = str(account_number).replace(" ", "")

    if account_str and not account_str.isdigit():
        masks_logger.error("Номер счета содержит нецифровые символы: %s", account_number)
        raise ValueError("Номер счета должен содержать только цифры")

    last_four = account_str[-4:]
    masked = f"**{last_four}"

    masks_logger.info("Номер счета успешно замаскирован: %s", masked)
    return masked
