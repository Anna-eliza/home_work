from unittest.mock import patch

import pytest

from src.main import (
    ask_yes_no,
    format_date,
    mask_account_or_card,
    print_transaction,
    read_csv_file,
    read_xlsx_file,
)


def test_read_csv_file_ok(csv_file):
    """Читает корректный CSV-файл."""
    result = read_csv_file(csv_file)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]['id'] == '1'
    assert result[0]['description'] == 'Открытие вклада'
    assert result[1]['currency'] == 'USD'


def test_read_csv_file_not_found(capsys):
    """Файл не найден → пустой список + сообщение."""
    result = read_csv_file('nonexistent.csv')
    captured = capsys.readouterr()

    assert result == []
    assert 'не найден' in captured.out


def test_read_csv_file_empty(tmp_path):
    """Пустой CSV-файл → пустой список."""
    file_path = tmp_path / 'empty.csv'
    file_path.write_text('id;state;description\n', encoding='utf-8')

    result = read_csv_file(str(file_path))
    assert result == []


def test_read_xlsx_file_ok(xlsx_file):
    """Читает корректный XLSX-файл."""
    result = read_xlsx_file(xlsx_file)

    assert len(result) == 1
    assert result[0]['id'] == 1
    assert result[0]['description'] == 'Открытие вклада'
    assert result[0]['currency'] == 'RUB'


def test_read_xlsx_file_not_found(capsys):
    """Файл не найден → пустой список + сообщение."""
    result = read_xlsx_file('nonexistent.xlsx')
    captured = capsys.readouterr()

    assert result == []
    assert 'не найден' in captured.out


@pytest.mark.parametrize('answer', ['да', 'ДА', 'Yes', 'y', 'д'])
def test_ask_yes_no_true(answer):
    """Ответ «Да» в разных формах → True."""
    with patch('builtins.input', return_value=answer):
        assert ask_yes_no('Prompt: ') is True


@pytest.mark.parametrize('answer', ['нет', 'НЕТ', 'No', 'n', 'н'])
def test_ask_yes_no_false(answer):
    """Ответ «Нет» в разных формах → False."""
    with patch('builtins.input', return_value=answer):
        assert ask_yes_no('Prompt: ') is False


def test_ask_yes_no_retry(capsys):
    """Некорректный ответ → повторный запрос."""
    answers = iter(['maybe', 'не знаю', 'да'])
    with patch('builtins.input', side_effect=lambda *_: next(answers)):
        result = ask_yes_no('Prompt: ')
    captured = capsys.readouterr()

    assert result is True
    assert captured.out.count('Пожалуйста, введите') == 2


def test_mask_account_or_card_account():
    """Маскировка счёта."""
    result = mask_account_or_card('Счет 12345678901234567890')

    assert result == 'Счет **7890'


def test_mask_account_or_card_account_lowercase():
    """Маскировка счёта со строчной буквы."""
    result = mask_account_or_card('счет 12345678901234567890')

    assert result == 'Счет **7890'


def test_mask_account_or_card_card():
    """Маскировка карты."""
    result = mask_account_or_card('MasterCard 7158300734726758')

    assert result == 'MasterCard 7158 30** **** 6758'


def test_mask_account_or_card_empty():
    """Пустая строка → пустая строка."""
    assert mask_account_or_card('') == ''



def test_format_date_iso():
    """ISO-дата → ДД.ММ.ГГГГ."""
    result = format_date('2019-12-08T22:46:21.935582')
    assert result == '08.12.2019'


def test_format_date_empty():
    """Пустая дата → пустая строка."""
    assert format_date('') == ''


def test_format_date_wrong_format():
    """Строка без дефисов возвращается как есть."""
    assert format_date('08.12.2019') == '08.12.2019'


def test_print_transaction_full(capsys):
    """Печать полной транзакции со счётом и картой."""
    transaction = {
        'date': '2019-11-12T10:00:00.000000',
        'description': 'Перевод с карты на карту',
        'from': 'MasterCard 7158300734726758',
        'to': 'Visa Platinum 1293387699203456',
        'amount': 130,
        'currency': 'USD',
    }
    print_transaction(transaction)
    captured = capsys.readouterr()

    assert '12.11.2019 Перевод с карты на карту' in captured.out
    assert 'MasterCard 7158 30** **** 6758' in captured.out
    assert 'Visa Platinum 1293 38** **** 3456' in captured.out
    assert 'Сумма: 130 USD' in captured.out


def test_print_transaction_rub(capsys):
    """RUB заменяется на «руб.»."""
    transaction = {
        'date': '2019-12-08T22:46:21',
        'description': 'Открытие вклада',
        'to': 'Счет 12345678901234567890',
        'amount': 40542,
        'currency': 'RUB',
    }
    print_transaction(transaction)
    captured = capsys.readouterr()

    assert '08.12.2019 Открытие вклада' in captured.out
    assert 'Счет **7890' in captured.out
    assert 'Сумма: 40542 руб.' in captured.out


def test_print_transaction_only_to(capsys):
    """Если нет from — печатается только to."""
    transaction = {
        'date': '2019-12-08T22:46:21',
        'description': 'Пополнение',
        'to': 'Счет 12345678901234567890',
        'amount': 100, 'currency': 'RUB',
    }
    print_transaction(transaction)
    captured = capsys.readouterr()

    assert '->' not in captured.out


def _run_main(inputs, monkeypatch, capsys):
    """Хелпер: запускает main() с заданной последовательностью вводов."""
    from src.main import main
    inputs_iter = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda *_: next(inputs_iter))
    main()
    return capsys.readouterr().out


def test_main_json_full_flow(
    monkeypatch, capsys, json_file, raw_json_transactions,
):
    """Полный сценарий: JSON → EXECUTED → без сортировки →
    без RUB → без поиска."""
    with patch('src.main.load_operations',
               return_value=raw_json_transactions):
        output = _run_main(
            ['1', json_file, 'EXECUTED', 'нет', 'нет', 'нет'],
            monkeypatch, capsys,
        )

    assert 'Добро пожаловать' in output
    assert 'Для обработки выбран JSON-файл.' in output
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in output
    assert 'Всего банковских операций в выборке: 3' in output


def test_main_csv_flow(monkeypatch, capsys, csv_file):
    """Полный сценарий через CSV."""
    output = _run_main(
        ['2', csv_file, 'executed', 'нет', 'нет', 'нет'],
        monkeypatch, capsys,
    )

    assert 'Для обработки выбран CSV-файл.' in output
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in output
    assert 'Всего банковских операций в выборке: 2' in output


def test_main_xlsx_flow(monkeypatch, capsys, xlsx_file):
    """Полный сценарий через XLSX."""
    output = _run_main(
        ['3', xlsx_file, 'EXECUTED', 'нет', 'нет', 'нет'],
        monkeypatch, capsys,
    )

    assert 'Для обработки выбран XLSX-файл.' in output
    assert 'Всего банковских операций в выборке: 1' in output


def test_main_invalid_status_then_valid(
    monkeypatch, capsys, json_file, raw_json_transactions,
):
    """Неверный статус → повторный запрос."""
    with patch('src.main.load_operations',
               return_value=raw_json_transactions):
        output = _run_main(
            ['1', json_file, 'test', 'EXECUTED',
             'нет', 'нет', 'нет'],
            monkeypatch, capsys,
        )

    assert 'Статус операции "TEST" недоступен.' in output
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in output


def test_main_invalid_menu_choice(
    monkeypatch, capsys, json_file, raw_json_transactions,
):
    """Неверный пункт меню → повторный запрос."""
    with patch('src.main.load_operations',
               return_value=raw_json_transactions):
        output = _run_main(
            ['9', '1', json_file, 'EXECUTED',
             'нет', 'нет', 'нет'],
            monkeypatch, capsys,
        )

    assert 'Некорректный выбор. Введите 1, 2 или 3.' in output


def test_main_sort_ascending(
    monkeypatch, capsys, json_file, raw_json_transactions,
):
    """Сортировка по возрастанию."""
    with patch('src.main.load_operations',
               return_value=raw_json_transactions):
        output = _run_main(
            ['1', json_file, 'EXECUTED',
             'да', 'по возрастанию', 'нет', 'нет'],
            monkeypatch, capsys,
        )

    assert output.index('18.07.2018') < output.index('08.12.2019')


def test_main_sort_descending(
    monkeypatch, capsys, json_file, raw_json_transactions,
):
    """Сортировка по убыванию."""
    with patch('src.main.load_operations',
               return_value=raw_json_transactions):
        output = _run_main(
            ['1', json_file, 'EXECUTED',
             'да', 'по убыванию', 'нет', 'нет'],
            monkeypatch, capsys,
        )

    assert output.index('08.12.2019') < output.index('18.07.2018')


def test_main_only_rub(
    monkeypatch, capsys, json_file, raw_json_transactions,
):
    """Только рублёвые транзакции."""
    with patch('src.main.load_operations',
               return_value=raw_json_transactions):
        output = _run_main(
            ['1', json_file, 'EXECUTED', 'нет', 'да', 'нет'],
            monkeypatch, capsys,
        )

    assert 'Всего банковских операций в выборке: 2' in output
    assert 'USD' not in output


def test_main_search_by_word(
    monkeypatch, capsys, json_file, raw_json_transactions,
):
    """Фильтр по слову в описании."""
    with patch('src.main.load_operations',
               return_value=raw_json_transactions):
        output = _run_main(
            ['1', json_file, 'EXECUTED', 'нет', 'нет',
             'да', 'вклада'],
            monkeypatch, capsys,
        )

    assert 'Всего банковских операций в выборке: 1' in output
    assert 'Открытие вклада' in output


def test_main_empty_result(
    monkeypatch, capsys, json_file, raw_json_transactions,
):
    """Пустая выборка → сообщение."""
    with patch('src.main.load_operations',
               return_value=raw_json_transactions):
        output = _run_main(
            ['1', json_file, 'EXECUTED', 'нет', 'нет',
             'да', 'Ипотека'],
            monkeypatch, capsys,
        )

    assert 'Не найдено ни одной транзакции' in output


def test_main_load_failed(monkeypatch, capsys):
    """Не удалось загрузить транзакции."""
    with patch('src.main.load_operations', return_value=[]):
        output = _run_main(
            ['1', 'missing.json'],
            monkeypatch, capsys,
        )

    assert 'Не удалось загрузить транзакции.' in output