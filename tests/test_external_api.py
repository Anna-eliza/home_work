from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


def test_convert_rub_no_api_call():
    """Проверяет, что для RUB функция возвращает сумму без вызова API."""
    transaction = {"amount": "5000", "currency": "RUB"}
    result = convert_to_rub(transaction)
    assert result == 5000.0


@patch("src.external_api.requests.get")
def test_convert_usd_to_rub(mock_get):
    """Тестирует конвертацию USD с мокированием ответа API."""
    # Настраиваем мок-ответ
    mock_response = Mock()
    mock_response.json.return_value = {"result": 9000.0}
    mock_response.raise_for_status.return_value = None  # Эмулируем успешный статус
    mock_get.return_value = mock_response

    transaction = {"amount": "100", "currency": "USD"}
    result = convert_to_rub(transaction)

    # Проверяем результат
    assert result == 9000.0

    # Проверяем, что API был вызван с правильными аргументами
    mock_get.assert_called_once()
    # Можно также проверить заголовки и параметры, если нужно
    args, kwargs = mock_get.call_args
    assert kwargs["params"]["from"] == "USD"
    assert kwargs["params"]["to"] == "RUB"
    assert kwargs["params"]["amount"] == 100.0


@patch("src.external_api.requests.get")
def test_convert_eur_to_rub(mock_get):
    """Тестирует конвертацию EUR."""
    mock_response = Mock()
    mock_response.json.return_value = {"result": 8500.0}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {"amount": "100", "currency": "EUR"}
    result = convert_to_rub(transaction)
    assert result == 8500.0
