import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_card_mask_standard_string(valid_card_16_digits, expected_card):
    assert get_mask_card_number(valid_card_16_digits) == expected_card


def test_card_mask_with_spaces(valid_card_with_spaces, expected_card):
    assert get_mask_card_number(valid_card_with_spaces) == expected_card


def test_card_mask_extra_prefix(card_with_extra_prefix):
    assert get_mask_card_number(card_with_extra_prefix) == "1234 56** **** 3456"


@pytest.mark.parametrize(
    "short_number, expected",
    [
        ("123456789012", "1234 56** **** 9012"),
        ("12345", "1234 5** **** 2345"),
        ("1234", "1234 ** **** 1234"),
        ("123", "123 ** **** 123"),
        ("1", "1 ** **** 1"),
    ],
)
def test_card_mask_short_numbers(short_number, expected):
    assert get_mask_card_number(short_number) == expected


def test_card_mask_empty_string():
    """Пустая строка — текущее поведение функции для карты."""
    assert get_mask_card_number("") == " ** **** "


def test_account_mask_standard_string(valid_account_20_digits, expected_account):
    assert get_mask_account(valid_account_20_digits) == expected_account


def test_account_mask_with_spaces(valid_account_with_spaces, expected_account):
    assert get_mask_account(valid_account_with_spaces) == expected_account


def test_account_mask_extra_prefix(account_with_extra_prefix):
    assert get_mask_account(account_with_extra_prefix) == "**7890"


@pytest.mark.parametrize(
    "account, expected",
    [
        ("1234567890", "**7890"),
        ("1234567", "**4567"),
        ("123456", "**3456"),
        ("12345", "**2345"),
        ("1234", "**1234"),
        ("123", "**123"),
        ("12", "**12"),
        ("1", "**1"),
    ],
)
def test_account_mask_various_lengths(account, expected):
    assert get_mask_account(account) == expected


def test_account_mask_empty_string():
    assert get_mask_account("") == "**"
