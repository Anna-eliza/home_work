from src.masks import get_mask_card_number, get_mask_account
from src.utils import load_operations

if __name__ == "__main__":
    # masks
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))

    try:
        get_mask_card_number("1234abcd5678efgh")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # utils
    load_operations("data/operations.json")
    load_operations("data/missing.json")