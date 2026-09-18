import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

def test_filter_by_currency_returns_iterator(transactions):
    result = filter_by_currency(transactions, "USD")
    assert iter(result) is result
    assert not isinstance(result, list)


def test_filter_by_currency_usd(transactions):
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 3
    assert [t["id"] for t in result] == [939719570, 142264268, 895315941]
    assert all(
        t["operationAmount"]["currency"]["code"] == "USD" for t in result
    )


def test_filter_by_currency_rub(transactions):
    result = list(filter_by_currency(transactions, "RUB"))
    assert [t["id"] for t in result] == [873106923, 594226727]


def test_filter_by_currency_does_not_mutate_input(transactions):
    original = list(transactions)
    list(filter_by_currency(transactions, "USD"))
    assert transactions == original


def test_transaction_descriptions_returns_all(transactions):
    result = list(transaction_descriptions(transactions))
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


def test_transaction_descriptions_length(transactions):
    assert len(list(transaction_descriptions(transactions))) == len(transactions)


def test_transaction_descriptions_first_five(transactions):
    descriptions = transaction_descriptions(transactions)
    result = [next(descriptions) for _ in range(5)]
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


def test_transaction_descriptions_types(transactions):
    assert all(isinstance(d, str) for d in transaction_descriptions(transactions))


def test_transaction_descriptions_original_order(transactions):
    expected = [t["description"] for t in transactions]
    assert list(transaction_descriptions(transactions)) == expected


def test_transaction_descriptions_empty_list():
    assert list(transaction_descriptions([])) == []


def test_transaction_descriptions_empty_list_stop_iteration():
    gen = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(gen)


@pytest.mark.parametrize(
    ("start", "end", "expected"),
    [
        (1, 5, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]),
        (1, 1, ["0000 0000 0000 0001"]),
        (10, 11, [
            "0000 0000 0000 0010",
            "0000 0000 0000 0011",
        ]),
        (9998, 10001, [
            "0000 0000 0000 9998",
            "0000 0000 0000 9999",
            "0000 0000 0001 0000",
            "0000 0000 0001 0001",
        ]),
        (9999_9999_9999_9999, 9999_9999_9999_9999, ["9999 9999 9999 9999"]),
        (9999_9999_9999_9997, 9999_9999_9999_9999, [
            "9999 9999 9999 9997",
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
        ]),
        (5, 1, []),
    ],
    ids=[
        "range-1-5",
        "single-value",
        "two-values",
        "cross-group-boundary",
        "max-boundary",
        "upper-boundary-slice",
        "empty-range",
    ],
)
def test_card_number_generator_range(transactions, start, end, expected):
    assert list(card_number_generator(start, end)) == expected


@pytest.mark.parametrize("number", [
    1,
    42,
    1000,
    1234_5678_9012_3456,
    9999_9999_9999_9999,
])
def test_card_number_generator_space_positions(transactions, number):
    card = next(card_number_generator(number, number))
    assert card[4] == " "
    assert card[9] == " "
    assert card[14] == " "






