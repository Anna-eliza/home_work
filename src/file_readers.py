"""Модуль для считывания финансовых операций из файлов CSV и XLSX."""

import csv
from pathlib import Path

import pandas as pd


def read_transactions_from_csv(file_path):
    """
    Считывает финансовые операции из CSV-файла.


    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    transactions = []

    with open(path, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(dict(row))

    return transactions


def read_transactions_from_excel(file_path):
    """
    Считывает финансовые операции из Excel-файла (.xlsx).

    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    dataframe = pd.read_excel(path, engine="openpyxl")

    dataframe = dataframe.where(pd.notnull(dataframe), None)

    transactions = dataframe.to_dict(orient="records")

    return transactions
