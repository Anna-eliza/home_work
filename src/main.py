import csv
from pathlib import Path

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency
from src.services import process_bank_search
from src.utils import load_operations


def read_csv_file(file_path: str) -> list[dict]:
    """Читает транзакции из CSV-файла."""
    transactions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                transactions.append(row)
    except FileNotFoundError:
        print(f'Файл не найден: {file_path}')
        return []
    return transactions


def read_xlsx_file(file_path: str) -> list[dict]:
    """Читает транзакции из XLSX-файла."""
    try:
        from openpyxl import load_workbook
    except ImportError:
        print('Установите openpyxl: pip install openpyxl')
        return []

    try:
        wb = load_workbook(file_path)
    except FileNotFoundError:
        print(f'Файл не найден: {file_path}')
        return []

    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    transactions = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        transactions.append(dict(zip(headers, row)))
    return transactions



def ask_yes_no(prompt: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ('да', 'yes', 'y', 'д'):
            return True
        if answer in ('нет', 'no', 'n', 'н'):
            return False
        print('Пожалуйста, введите "Да" или "Нет".')


def mask_account_or_card(value: str) -> str:
    """Маскирует номер счёта или карты."""
    if not value:
        return ''

    if value.lower().startswith('счет'):
        digits = ''.join(ch for ch in value if ch.isdigit())
        return f'Счет **{digits[-4:]}'

    return get_mask_card_number(value)


def format_date(date_raw: str) -> str:
    """Преобразует дату ISO в формат ДД.ММ.ГГГГ."""
    if not date_raw:
        return ''
    date = date_raw[:10]
    if '-' in date:
        y, m, d = date.split('-')
        return f'{d}.{m}.{y}'
    return date


def print_transaction(transaction: dict) -> None:
    """Печатает одну транзакцию в читаемом виде."""
    date = format_date(transaction.get('date', ''))
    description = transaction.get('description', '')
    from_acc = transaction.get('from', '')
    to_acc = transaction.get('to', '')
    amount = transaction.get('amount', '')
    currency = transaction.get('currency', '')

    print(f'{date} {description}')

    if from_acc and to_acc:
        print(f'{mask_account_or_card(from_acc)} -> '
              f'{mask_account_or_card(to_acc)}')
    elif to_acc:
        print(mask_account_or_card(to_acc))

    currency_suffix = 'руб.' if currency == 'RUB' else currency
    print(f'Сумма: {amount} {currency_suffix}\n')



def main() -> None:
    """Основная функция проекта: связывает всю логику вместе."""
    print('Привет! Добро пожаловать в программу работы '
          'с банковскими транзакциями.')
    print('Выберите необходимый пункт меню:')
    print('1. Получить информацию о транзакциях из JSON-файла')
    print('2. Получить информацию о транзакциях из CSV-файла')
    print('3. Получить информацию о транзакциях из XLSX-файла')

    while True:
        choice = input().strip()

        if choice == '1':
            print('Для обработки выбран JSON-файл.')
            file_path = input('Введите путь к JSON-файлу: ').strip()
            transactions = load_operations(file_path)
            break

        elif choice == '2':
            print('Для обработки выбран CSV-файл.')
            file_path = input('Введите путь к CSV-файлу: ').strip()
            transactions = read_csv_file(file_path)
            break

        elif choice == '3':
            print('Для обработки выбран XLSX-файл.')
            file_path = input('Введите путь к XLSX-файлу: ').strip()
            transactions = read_xlsx_file(file_path)
            break

        else:
            print('Некорректный выбор. Введите 1, 2 или 3.')

    if not transactions:
        print('Не удалось загрузить транзакции.')
        return


    available_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        print('Введите статус, по которому необходимо выполнить '
              'фильтрацию.')
        print(f'Доступные для фильтровки статусы: '
              f'{", ".join(available_statuses)}')

        user_status = input().strip().upper()

        if user_status in available_statuses:
            print(f'Операции отфильтрованы по статусу "{user_status}"')
            break

        print(f'Статус операции "{user_status}" недоступен.')

    transactions = filter_by_state(transactions, user_status)


    if ask_yes_no('Отсортировать операции по дате? Да/Нет\n'):
        order = input(
            'Отсортировать по возрастанию или по убыванию?\n'
        ).strip().lower()

        if order in ('по возрастанию', 'возрастание', 'asc'):
            transactions = sort_by_date(transactions, reverse=False)
        elif order in ('по убыванию', 'убывание', 'desc'):
            transactions = sort_by_date(transactions, reverse=True)
        else:
            print('Некорректный ввод, сортировка не применена.')


    if ask_yes_no('Выводить только рублевые транзакции? Да/Нет\n'):
        transactions = filter_by_currency(transactions, 'RUB')


    if ask_yes_no(
        'Отфильтровать список транзакций по определенному слову '
        'в описании? Да/Нет\n'
    ):
        search = input('Введите слово для поиска: ').strip()
        transactions = process_bank_search(transactions, search)


    print('Распечатываю итоговый список транзакций...')

    if not transactions:
        print('Не найдено ни одной транзакции, подходящей под ваши '
              'условия фильтрации')
        return

    print(f'\nВсего банковских операций в выборке: '
          f'{len(transactions)}\n')

    for transaction in transactions:
        print_transaction(transaction)


if __name__ == '__main__':
    main()