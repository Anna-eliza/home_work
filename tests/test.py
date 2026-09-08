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

from src.widget import mask_account_card
test_inputs = [
    "Maestro 1596837868705199",
    "Счет 64686473678894779589",
    "MasterCard 7158300734726758",
    "Счет 35383033474447895560",
    "Visa Classic 6831982476737658",
    "Visa Platinum 8990922113665229",
    "Visa Gold 5999414228426353",
    "Счет 73654108430135874305"
]

print("РЕЗУЛЬТАТЫ РАБОТЫ ФУНКЦИИ mask_account_card")
print("=" * 50)

for input_str in test_inputs:
    result = mask_account_card(input_str)
    print(f"{input_str} → {result}")

print("=" * 50)


