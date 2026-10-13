from src.services import process_bank_operations, process_bank_search


def test_search_finds_matching_transactions(sample_transactions):
    """Находит транзакции по подстроке в описании."""
    result = process_bank_search(sample_transactions, "Перевод")

    assert len(result) == 3
    assert all("Перевод" in t["description"] for t in result)
    assert [t["id"] for t in result] == [1, 3, 6]


def test_search_case_insensitive(sample_transactions):
    """Поиск не зависит от регистра."""
    result_lower = process_bank_search(sample_transactions, "перевод")
    result_upper = process_bank_search(sample_transactions, "ПЕРЕВОД")
    result_mixed = process_bank_search(sample_transactions, "ПЕрЕвОд")

    assert len(result_lower) == 3
    assert result_lower == result_upper == result_mixed


def test_search_partial_match(sample_transactions):
    """Поиск по части слова."""
    result = process_bank_search(sample_transactions, "карт")

    assert len(result) == 2
    assert {t["id"] for t in result} == {1, 3}


def test_search_no_matches(sample_transactions):
    """Возвращает пустой список, если совпадений нет."""
    result = process_bank_search(sample_transactions, "Ипотека")

    assert result == []


def test_search_empty_string(sample_transactions):
    """Пустая строка поиска → пустой результат."""
    result = process_bank_search(sample_transactions, "")

    assert result == []


def test_search_empty_data():
    """Пустой список данных → пустой результат."""
    result = process_bank_search([], "Перевод")

    assert result == []


def test_search_missing_description_key(
    sample_transactions_without_description,
):
    """Транзакция без ключа description не падает."""
    result = process_bank_search(sample_transactions_without_description, "Перевод")

    assert len(result) == 2
    assert [t["id"] for t in result] == [2, 3]


def test_search_regex_special_chars(
    sample_transactions_with_special_chars,
):
    """Спецсимволы regex в поисковой строке экранируются."""
    result = process_bank_search(sample_transactions_with_special_chars, "(внутренний)")

    assert len(result) == 1
    assert result[0]["id"] == 1

    result_dot = process_bank_search(sample_transactions_with_special_chars, "100.50")
    assert len(result_dot) == 1
    assert result_dot[0]["id"] == 3


def test_search_returns_original_objects(sample_transactions):
    """Возвращаются те же объекты, а не копии."""
    result = process_bank_search(sample_transactions, "Оплата")

    for transaction in result:
        assert transaction in sample_transactions


def test_operations_counts_all_categories(sample_transactions):
    """Считает количество операций по каждой категории."""
    categories = ["Перевод", "Оплата", "Снятие"]
    result = process_bank_operations(sample_transactions, categories)

    assert result == {"Перевод": 3, "Оплата": 2, "Снятие": 1}


def test_operations_zero_for_missing_category(sample_transactions):
    """Категория без совпадений попадает в результат со значением 0."""
    categories = ["Перевод", "Пополнение", "Ипотека"]
    result = process_bank_operations(sample_transactions, categories)

    assert result == {"Перевод": 3, "Пополнение": 0, "Ипотека": 0}


def test_operations_empty_categories(sample_transactions):
    """Пустой список категорий → пустой словарь."""
    result = process_bank_operations(sample_transactions, [])

    assert result == {}


def test_operations_empty_data():
    """Пустой список транзакций → все категории по 0."""
    categories = ["Перевод", "Оплата"]
    result = process_bank_operations([], categories)

    assert result == {"Перевод": 0, "Оплата": 0}


def test_operations_missing_description_key(
    sample_transactions_without_description,
):
    """Транзакции без description не считаются."""
    result = process_bank_operations(sample_transactions_without_description, ["Перевод"])

    assert result == {"Перевод": 2}


def test_operations_transaction_in_multiple_categories():
    """Одна транзакция может попасть в несколько категорий."""
    data = [
        {"id": 1, "description": "Перевод и оплата услуг"},
    ]
    categories = ["Перевод", "Оплата"]
    result = process_bank_operations(data, categories)

    assert result == {"Перевод": 1, "Оплата": 1}


def test_operations_case_insensitive(sample_transactions):
    """Подсчёт не зависит от регистра (аналогично поиску)."""
    result_lower = process_bank_operations(sample_transactions, ["перевод"])
    result_upper = process_bank_operations(sample_transactions, ["ПЕРЕВОД"])
    result_mixed = process_bank_operations(sample_transactions, ["ПеРеВоД"])

    assert result_lower == {"перевод": 3}
    assert result_upper == {"ПЕРЕВОД": 3}
    assert result_mixed == {"ПеРеВоД": 3}


def test_operations_returns_dict(sample_transactions):
    """Возвращает именно dict, а не Counter."""
    categories = ["Перевод"]
    result = process_bank_operations(sample_transactions, categories)

    assert isinstance(result, dict)
    assert not hasattr(result, "most_common")


def test_operations_no_duplicates_in_categories(sample_transactions):
    """Дубликаты категорий не ломают логику."""
    categories = ["Перевод", "Перевод", "Оплата"]
    result = process_bank_operations(sample_transactions, categories)

    assert result == {"Перевод": 3, "Оплата": 2}


def test_search_then_operations(sample_transactions):
    """Сначала фильтруем, потом считаем категории."""
    filtered = process_bank_search(sample_transactions, "карт")
    result = process_bank_operations(filtered, ["Перевод", "Оплата"])

    assert result == {"Перевод": 2, "Оплата": 0}
