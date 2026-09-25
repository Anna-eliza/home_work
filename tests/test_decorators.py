import pytest

from src.decorators import log


def test_console_success(capsys):
    """Успешный вызов без filename пишет в консоль имя функции и результат."""

    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5

    captured = capsys.readouterr()
    assert "add" in captured.out
    assert "5" in captured.out
    assert "успешно" in captured.out.lower() or "результат" in captured.out.lower()


def test_console_error(capsys):
    """Ошибка без filename пишет в консоль имя функции, тип ошибки и параметры."""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "1" in captured.out
    assert "0" in captured.out


def test_console_error_with_kwargs(capsys):
    """Проверяем, что именованные аргументы тоже попадают в лог ошибки."""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(a=10, b=0)

    captured = capsys.readouterr()
    assert "divide" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "10" in captured.out
    assert "0" in captured.out


def test_file_success(tmp_path):
    """Успешный вызов с filename пишет в файл."""

    log_file = tmp_path / "success.log"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    result = multiply(4, 5)

    assert result == 20
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "multiply" in content
    assert "20" in content


def test_file_error(tmp_path):
    """Ошибка с filename пишет в файл имя функции, тип ошибки и параметры."""

    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(7, 0)

    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "divide" in content
    assert "ZeroDivisionError" in content
    assert "7" in content
    assert "0" in content


def test_file_appends_multiple_calls(tmp_path):
    """Несколько вызовов дописываются, а не перезаписывают файл."""

    log_file = tmp_path / "multi.log"

    @log(filename=str(log_file))
    def add(a, b):
        return a + b

    add(1, 1)
    add(2, 2)
    add(3, 3)

    content = log_file.read_text(encoding="utf-8")
    assert "2" in content
    assert "4" in content
    assert "6" in content


def test_exception_propagates(capsys):
    """Исключение не проглатывается декоратором, а вылетает наружу."""

    @log()
    def broken():
        raise ValueError("специально сломано")

    with pytest.raises(ValueError, match="специально сломано"):
        broken()

    captured = capsys.readouterr()
    assert "ValueError" in captured.out


def test_exception_propagates_file(tmp_path):
    """То же для варианта с файлом."""

    log_file = tmp_path / "propagate.log"

    @log(filename=str(log_file))
    def broken():
        raise KeyError("нет ключа")

    with pytest.raises(KeyError):
        broken()


def test_preserves_name_and_doc(capsys):
    """@wraps сохраняет __name__ и __doc__ исходной функции."""

    @log()
    def documented():
        """Это докстринг."""
        return 1

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Это докстринг."
