"""Тесты для модуля file_readers."""

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.file_readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)


class TestReadTransactionsFromCsv:
    """Тесты чтения CSV через реальные файлы (фикстуры из conftest)."""

    def test_returns_list(self, csv_file):
        result = read_transactions_from_csv(csv_file)
        assert isinstance(result, list)

    def test_returns_list_of_dicts(self, csv_file):
        result = read_transactions_from_csv(csv_file)
        assert all(isinstance(item, dict) for item in result)

    def test_count_matches(self, csv_file, sample_transactions):
        result = read_transactions_from_csv(csv_file)
        assert len(result) == len(sample_transactions)

    def test_content_matches(self, csv_file, sample_transactions):
        result = read_transactions_from_csv(csv_file)
        assert result == sample_transactions

    def test_keys_present(self, csv_file):
        result = read_transactions_from_csv(csv_file)
        assert set(result[0].keys()) == {"id", "amount", "category", "date"}

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            read_transactions_from_csv(tmp_path / "no_such_file.csv")

    def test_accepts_string_path(self, csv_file_path_str):
        result = read_transactions_from_csv(csv_file_path_str)
        assert len(result) > 0

    def test_accepts_path_object(self, csv_file):
        result = read_transactions_from_csv(Path(csv_file))
        assert len(result) > 0

    def test_empty_csv(self, tmp_path):
        file_path = tmp_path / "empty.csv"
        file_path.write_text("id,amount\n", encoding="utf-8")
        assert read_transactions_from_csv(file_path) == []


class TestReadTransactionsFromCsvWithMock:
    """Тесты чтения CSV с подменой open() и csv.DictReader."""

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.csv.DictReader")
    @patch("builtins.open", new_callable=mock_open)
    def test_uses_dictreader(self, mock_file, mock_reader_cls, mock_exists):
        """Проверяем, что функция использует csv.DictReader."""
        mock_reader = MagicMock()
        mock_reader.__iter__ = MagicMock(
            return_value=iter(
                [
                    {"id": "1", "amount": "100", "category": "Еда", "date": "2024-01-01"},
                    {"id": "2", "amount": "200", "category": "Транспорт", "date": "2024-01-02"},
                ]
            )
        )
        mock_reader_cls.return_value = mock_reader

        result = read_transactions_from_csv("fake.csv")

        mock_reader_cls.assert_called_once()
        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["category"] == "Транспорт"

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.csv.DictReader")
    @patch("builtins.open", new_callable=mock_open)
    def test_returns_empty_list_when_no_rows(self, mock_file, mock_reader_cls, mock_exists):
        """Если DictReader не отдаёт строк — результат пустой список."""
        mock_reader = MagicMock()
        mock_reader.__iter__ = MagicMock(return_value=iter([]))
        mock_reader_cls.return_value = mock_reader

        result = read_transactions_from_csv("fake.csv")
        assert result == []

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.csv.DictReader")
    @patch("builtins.open", new_callable=mock_open)
    def test_converts_rows_to_plain_dicts(self, mock_file, mock_reader_cls, mock_exists):
        """Строки преобразуются в обычные dict."""
        mock_reader = MagicMock()
        mock_reader.__iter__ = MagicMock(
            return_value=iter(
                [
                    {"id": "1", "amount": "100"},
                ]
            )
        )
        mock_reader_cls.return_value = mock_reader

        result = read_transactions_from_csv("fake.csv")
        assert type(result[0]) is dict

    @patch("src.file_readers.Path.exists", return_value=False)
    def test_raises_when_path_missing(self, mock_exists):
        """Если путь не существует — FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_transactions_from_csv("any.csv")

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.csv.DictReader")
    @patch("builtins.open", new_callable=mock_open)
    def test_open_called_with_utf8(self, mock_file, mock_reader_cls, mock_exists):
        """open() вызывается с encoding='utf-8' и режимом 'r'."""
        mock_reader = MagicMock()
        mock_reader.__iter__ = MagicMock(return_value=iter([]))
        mock_reader_cls.return_value = mock_reader

        read_transactions_from_csv("fake.csv")

        mock_file.assert_called_once()
        args, kwargs = mock_file.call_args

        assert Path(args[0]) == Path("fake.csv")
        assert kwargs.get("encoding") == "utf-8"

        mode = kwargs.get("mode") or (args[1] if len(args) > 1 else None)
        assert mode == "r"


class TestReadTransactionsFromExcel:
    """Тесты чтения XLSX через реальные файлы (фикстуры из conftest)."""

    def test_returns_list(self, xlsx_file):
        result = read_transactions_from_excel(xlsx_file)
        assert isinstance(result, list)

    def test_returns_list_of_dicts(self, xlsx_file):
        result = read_transactions_from_excel(xlsx_file)
        assert all(isinstance(item, dict) for item in result)

    def test_count_matches(self, xlsx_file, sample_transactions):
        result = read_transactions_from_excel(xlsx_file)
        assert len(result) == len(sample_transactions)

    def test_keys_present(self, xlsx_file):
        result = read_transactions_from_excel(xlsx_file)
        assert set(result[0].keys()) == {"id", "amount", "category", "date"}

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            read_transactions_from_excel(tmp_path / "no_such_file.xlsx")

    def test_accepts_string_path(self, xlsx_file_path_str):
        result = read_transactions_from_excel(xlsx_file_path_str)
        assert len(result) > 0

    def test_accepts_path_object(self, xlsx_file):
        result = read_transactions_from_excel(Path(xlsx_file))
        assert len(result) > 0


class TestReadTransactionsFromExcelWithMock:
    """Тесты чтения Excel с подменой pd.read_excel."""

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.pd.read_excel")
    def test_calls_read_excel_with_openpyxl(self, mock_read_excel, mock_exists):
        """pd.read_excel вызывается с engine='openpyxl'."""
        mock_read_excel.return_value = pd.DataFrame(
            [
                {"id": "1", "amount": "100", "category": "Еда", "date": "2024-01-01"},
            ]
        )

        result = read_transactions_from_excel("fake.xlsx")

        mock_read_excel.assert_called_once()
        _, kwargs = mock_read_excel.call_args
        assert kwargs.get("engine") == "openpyxl"
        assert len(result) == 1
        assert result[0]["id"] == "1"

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.pd.read_excel")
    def test_returns_list_of_dicts(self, mock_read_excel, mock_exists):
        """Результат — список словарей."""
        mock_read_excel.return_value = pd.DataFrame(
            [
                {"id": "1", "amount": "100"},
                {"id": "2", "amount": "200"},
            ]
        )

        result = read_transactions_from_excel("fake.xlsx")
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.pd.read_excel")
    def test_nan_replaced_with_none(self, mock_read_excel, mock_exists):
        """NaN-значения заменяются на None."""
        mock_read_excel.return_value = pd.DataFrame(
            [
                {"id": "1", "amount": None, "category": "Еда"},
            ]
        )

        result = read_transactions_from_excel("fake.xlsx")
        assert result[0]["amount"] is None

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.pd.read_excel")
    def test_empty_dataframe(self, mock_read_excel, mock_exists):
        """Пустой DataFrame → пустой список."""
        mock_read_excel.return_value = pd.DataFrame()
        result = read_transactions_from_excel("fake.xlsx")
        assert result == []

    @patch("src.file_readers.Path.exists", return_value=False)
    def test_raises_when_path_missing(self, mock_exists):
        """Если путь не существует — FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_transactions_from_excel("any.xlsx")

    @patch("src.file_readers.Path.exists", return_value=True)
    @patch("src.file_readers.pd.read_excel")
    def test_uses_orient_records(self, mock_read_excel, mock_exists):
        """to_dict вызывается с orient='records' (проверяем через структуру)."""
        mock_read_excel.return_value = pd.DataFrame(
            [
                {"id": "1", "amount": "100"},
                {"id": "2", "amount": "200"},
            ]
        )
        result = read_transactions_from_excel("fake.xlsx")
        # Если orient='records' — получим список словарей, а не словарь списков
        assert isinstance(result, list)
        assert result[0]["id"] == "1"
