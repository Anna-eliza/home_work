def get_mask_card_number(card_number: str | int) -> str:
    """Функция маскирует номер карты клиента"""

    card_str = str(card_number).replace(" ", "")
    card_str = card_str[-16:]
    first_six = card_str[:6]
    last_four = card_str[-4:]
    return f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"


def get_mask_account(account_number: str | int) -> str:
    """Функция маскирует номер банковского счета"""

    account_str = str(account_number).replace(" ", "")
    last_four = account_str[-4:]
    return f"**{last_four}"
