import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_standard(account_input_standard):
    assert mask_account_card(account_input_standard) == "Счет **7890"


def test_mask_account_with_spaces(account_input_with_spaces):
    assert mask_account_card(account_input_with_spaces) == "Счет **7890"


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Счет 1234", "Счет **1234"),
        ("Счет 1", "Счет **1"),
    ],
)
def test_mask_account_various_lengths(input_string, expected):
    assert mask_account_card(input_string) == expected


def test_mask_card_simple_name(card_input_simple_name):
    assert mask_account_card(card_input_simple_name) == "Visa 1234 56** **** 3456"


def test_mask_card_two_words(card_input_two_words):
    assert mask_account_card(card_input_two_words) == "Visa Platinum 1234 56** **** 3456"


def test_mask_card_three_words(card_input_three_words):
    assert mask_account_card(card_input_three_words) == "Maestro Classic Debit 1234 56** **** 3456"


def test_mask_input_is_single_token_with_number():
    assert mask_account_card("1234567890123456") == "1234567890123456"


def test_get_date_full_iso(iso_datetime_full):
    assert get_date(iso_datetime_full) == "15.03.2024"


def test_get_date_without_time(iso_date_only):
    assert get_date(iso_date_only) == "15.03.2024"


def test_get_date_without_microseconds(iso_datetime_no_microseconds):
    assert get_date(iso_datetime_no_microseconds) == "15.03.2024"


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("2024-01-01T00:00:00", "01.01.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2025-06-10T12:00:00", "10.06.2025"),
        ("2000-02-29T08:15:00", "29.02.2000"),
    ],
)
def test_get_date_various_dates(input_string, expected):
    assert get_date(input_string) == expected
