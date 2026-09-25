import pytest


@pytest.fixture
def valid_card_16_digits():
    return "1234567890123456"


@pytest.fixture
def valid_card_with_spaces():
    return "1234 5678 9012 3456"


@pytest.fixture
def card_with_extra_prefix():
    return "99991234567890123456"


@pytest.fixture
def expected_card():
    return "1234 56** **** 3456"


@pytest.fixture
def valid_account_20_digits():
    return "12345678901234567890"


@pytest.fixture
def valid_account_with_spaces():
    return "1234 5678 9012 3456 7890"


@pytest.fixture
def account_with_extra_prefix():
    return "99999912345678901234567890"


@pytest.fixture
def expected_account():
    return "**7890"


@pytest.fixture
def operations_mixed_states():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-15"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-10"},
        {"id": 3, "state": "EXECUTED", "date": "2024-05-20"},
        {"id": 4, "state": "PENDING", "date": "2024-02-01"},
        {"id": 5, "state": "EXECUTED", "date": "2024-04-05"},
    ]


@pytest.fixture
def operations_only_executed():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-15"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-10"},
    ]


@pytest.fixture
def operations_without_state_key():
    return [
        {"id": 1, "date": "2024-03-15"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-10"},
    ]


@pytest.fixture
def operations_with_same_dates():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-15"},
        {"id": 2, "state": "CANCELED", "date": "2024-03-15"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-15"},
    ]


@pytest.fixture
def operations_unsorted():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-15"},
        {"id": 2, "state": "EXECUTED", "date": "2023-12-01"},
        {"id": 3, "state": "EXECUTED", "date": "2025-06-10"},
        {"id": 4, "state": "EXECUTED", "date": "2024-01-05"},
    ]


@pytest.fixture
def operations_different_date_formats():
    return [
        {"id": 1, "state": "EXECUTED", "date": "15.03.2024"},
        {"id": 2, "state": "EXECUTED", "date": "2024-03-15"},
        {"id": 3, "state": "EXECUTED", "date": "01.01.2024"},
    ]


@pytest.fixture
def empty_operations():
    return []


@pytest.fixture
def account_input_standard():
    return "Счет 12345678901234567890"


@pytest.fixture
def account_input_with_spaces():
    return "Счет 1234 5678 9012 3456 7890"


@pytest.fixture
def card_input_simple_name():
    return "Visa 1234567890123456"


@pytest.fixture
def card_input_two_words():
    return "Visa Platinum 1234567890123456"


@pytest.fixture
def card_input_three_words():
    return "Maestro Classic Debit 1234567890123456"


@pytest.fixture
def iso_datetime_full():
    return "2024-03-15T10:30:00.000000"


@pytest.fixture
def iso_date_only():
    return "2024-03-15"


@pytest.fixture
def iso_datetime_no_microseconds():
    return "2024-03-15T10:30:00"
