"""Модуль с итераторами чисел Фибоначчи."""

from typing import Iterable, Iterator, List


def is_fibonacci_number(x: int) -> bool:
    """
    Проверяет, является ли число числом Фибоначчи.

    N является числом Фибоначчи тогда и только тогда,
    когда 5*N^2 + 4 или 5*N^2 - 4 является полным квадратом.
    """
    if x < 0:
        return False

    def is_square(num: int) -> bool:
        root: int = int(num ** 0.5)
        return root * root == num

    return is_square(5 * x * x + 4) or is_square(5 * x * x - 4)


class FibonacchiLst:
    """
    Итератор принимает список чисел и при переборе возвращает
    только те числа, которые являются числами Фибоначчи.

    Реализован через __iter__ и __next__.

        list(FibonacchiLst([0, 1, 2, 3, 4, 5]))
        -> [0, 1, 2, 3, 5]
    """

    def __init__(self, data: Iterable[int]) -> None:
        self.data: List[int] = list(data)
        self.index: int = 0

    def __iter__(self) -> "FibonacchiLst":
        """Возвращает сам объект как итератор."""
        return self

    def __next__(self) -> int:
        """Возвращает следующее число Фибоначчи или вызывает StopIteration."""
        while self.index < len(self.data):
            current_value: int = self.data[self.index]
            self.index += 1
            if is_fibonacci_number(current_value):
                return current_value
        raise StopIteration


class FibonacchiLstGetItem:
    """
    Упрощённый итератор через __getitem__.

    Python автоматически создаёт итератор для объектов,
    у которых реализован __getitem__, начиная с индекса 0.

        list(FibonacchiLstGetItem([0, 1, 2, 3, 4, 5]))
        -> [0, 1, 2, 3, 5]
    """

    def __init__(self, data: Iterable[int]) -> None:
        # Оставляем только числа Фибоначчи сразу при инициализации
        self.data: List[int] = [x for x in data if is_fibonacci_number(x)]

    def __getitem__(self, index: int) -> int:
        """Возвращает элемент по индексу или вызывает IndexError."""
        return self.data[index]


if __name__ == '__main__':
    sample = list(range(10))
    print("FibonacchiLst:       ", list(FibonacchiLst(sample)))
    print("FibonacchiLstGetItem:", list(FibonacchiLstGetItem(sample)))
