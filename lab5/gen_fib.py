"""Модуль с реализацией генератора чисел Фибоначчи и сопрограммы."""

import functools
import itertools
from typing import Generator, List, Any

def fib_elem_gen() -> Generator[int, None, None]:
    """Генератор, бесконечно возвращающий элементы ряда Фибоначчи."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def fib_coroutine(g: Any) -> Any:
    """Декоратор для инициализации (priming) сопрограммы."""
    @functools.wraps(g)
    def inner(*args: Any, **kwargs: Any) -> Generator:
        gen = g(*args, **kwargs)
        gen.send(None) # Запускаем сопрограмму до первого yield
        return gen
    return inner

@fib_coroutine
def my_genn() -> Generator[List[int], int, None]:
    """
    Сопрограмма, возвращающая список из n чисел Фибоначчи.
    
    Ожидает получение числа n через метод send(n).
    """
    n = yield [] # Первичное ожидание после send(None)
    
    while True:
        if n is not None and n > 0:
            # Получаем ровно n элементов из бесконечного генератора
            result = list(itertools.islice(fib_elem_gen(), n))
        else:
            result = []
            
        # Отдаем результат и тут же ждем новое значение n
        n = yield result

if __name__ == '__main__':
    gen = my_genn()
    print("Сопрограмма: send(3) ->", gen.send(3))
    print("Сопрограмма: send(5) ->", gen.send(5))
    print("Сопрограмма: send(8) ->", gen.send(8))
