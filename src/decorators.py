from functools import wraps


def log(filename=None):
    def write_log(message):
        """Пишет сообщение в файл, если filename задан, иначе — в консоль."""
        if filename is None:
            print(message)
        else:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(message + "\n")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            write_log(f"Начало выполнения функции {func.__name__}")
            try:
                result = func(*args, **kwargs)
                write_log(
                    f"Функция {func.__name__} выполнилась успешно. "
                    f"Результат: {result}"
                )
                return result
            except Exception as e:
                write_log(
                    f"Функция {func.__name__} вызвала ошибку "
                    f"{type(e).__name__}. "
                    f"Входные параметры: args={args}, kwargs={kwargs}"
                )
                raise
            finally:
                write_log(f"Конец выполнения функции {func.__name__}")

        return wrapper

    return decorator

if __name__ == "__main__":
    @log(filename="mylog.txt")
    def my_function(x, y):
        return x + y

    my_function(1, 2)
