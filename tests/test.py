from src.masks import get_mask_account, get_mask_card_number

card_number = "7000792289606361"
masked_card = get_mask_card_number(card_number)
print(f"Номер карты: {card_number}")
print(f"Маска карты: {masked_card}")
print("-------")

account_number = "73654108430135874305"
masked_account = get_mask_account(account_number)
print(f"Номер счета: {account_number}")
print(f"Маска счета: {masked_account}")
print()