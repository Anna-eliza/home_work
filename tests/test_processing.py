import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_default_state(operations_mixed_states):
    result = filter_by_state(operations_mixed_states)
    assert len(result) == 3
    assert all(item["state"] == "EXECUTED" for item in result)


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
    ],
)
def test_filter_by_various_states(operations_mixed_states, state, expected_ids):
    result = filter_by_state(operations_mixed_states, state=state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_returns_empty_when_no_match(operations_mixed_states):
    result = filter_by_state(operations_mixed_states, state="UNKNOWN")
    assert result == []


def test_filter_does_not_mutate_input(operations_mixed_states):
    original = [dict(item) for item in operations_mixed_states]
    filter_by_state(operations_mixed_states, state="EXECUTED")
    assert operations_mixed_states == original


def test_filter_all_executed(operations_only_executed):
    result = filter_by_state(operations_only_executed)
    assert result == operations_only_executed


def test_filter_skips_dicts_without_state_key(operations_without_state_key):
    result = filter_by_state(operations_without_state_key)
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_empty_list(empty_operations):
    assert filter_by_state(empty_operations) == []


def test_filter_case_sensitive(operations_mixed_states):
    result = filter_by_state(operations_mixed_states, state="executed")
    assert result == []


def test_sort_by_date_descending_default(operations_unsorted):
    result = sort_by_date(operations_unsorted)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(operations_unsorted):
    result = sort_by_date(operations_unsorted, reverse=False)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates)


def test_sort_does_not_mutate_input(operations_unsorted):
    original = [dict(item) for item in operations_unsorted]
    sort_by_date(operations_unsorted)
    assert operations_unsorted == original


def test_sort_with_same_dates(operations_with_same_dates):
    result = sort_by_date(operations_with_same_dates)
    ids = [item["id"] for item in result]
    assert ids == [1, 2, 3]


def test_sort_empty_list(empty_operations):
    assert sort_by_date(empty_operations) == []


def test_sort_different_date_formats(operations_different_date_formats):
    result = sort_by_date(operations_different_date_formats)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)
