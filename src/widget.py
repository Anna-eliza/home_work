from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(input_string: str) -> str:
    """Маскирует номер карты или счета, в зависимости от типа"""
    if "Счет" in input_string:
        parts = input_string.split(maxsplit=1)
        if len(parts) != 2:
            return input_string
        account_type = parts[0]
        account_number = parts[1]
        masked_number = get_mask_account(account_number)
        return f"{account_type} {masked_number}"
    else:
        parts = input_string.rsplit(maxsplit=1)
        if len(parts) != 2:
            return input_string
        card_name = parts[0]
        card_number = parts[1]
        masked_number = get_mask_card_number(card_number)
        return f"{card_name} {masked_number}"

def get_date(date_string: str) -> str:
    """ сокращает формат даты на банковской карте"""
    date_part = date_string.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"
