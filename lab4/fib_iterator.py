"""Модуль с реализацией итераторов для фильтрации чисел Фибоначчи из списка."""

import math
from typing import List, Any

def is_fibonacci(n: Any) -> bool:
    """Проверяет, является ли число элементом ряда Фибоначчи."""
    if not isinstance(n, int) or n < 0:
        return False
    
    def is_perfect_square(x: int) -> bool:
        s = int(math.isqrt(x))
        return s * s == x
        
    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)

class FibonacchiLst:
    """
    Итератор (обычный способ через __iter__ и __next__).
    Возвращает элементы из переданного списка, принадлежащие ряду Фибоначчи.
    """
    def __init__(self, instance: List[int]):
        self.instance = instance
        self.idx = 0

    def __iter__(self) -> 'FibonacchiLst':
        """Возвращает экземпляр итератора."""
        return self

    def __next__(self) -> int:
        """Возвращает следующий элемент, являющийся числом Фибоначчи."""
        while True:
            try:
                res = self.instance[self.idx]
            except IndexError:
                raise StopIteration

            self.idx += 1
            if is_fibonacci(res):
                return res

class FibonacchiLstGetItem:
    """
    Итератор (упрощенный способ через __getitem__).
    Реализует протокол итерации без сохранения внутреннего состояния.
    """
    def __init__(self, instance: List[int]):
        self.instance = instance

    def __getitem__(self, item: int) -> int:
        """
        Динамически ищет item-ное по счету число Фибоначчи в списке.
        Вызывается под капотом при использовании list(), for и т.д.
        """
        count = -1
        for val in self.instance:
            if is_fibonacci(val):
                count += 1
                if count == item:
                    return val
        raise IndexError("Index out of range for Fibonacci items")
