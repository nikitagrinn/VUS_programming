"""Тесты для классов-итераторов."""

import unittest
from fib_iterator import FibonacchiLst, FibonacchiLstGetItem

class TestFibIterator(unittest.TestCase):
    """Тесты для обычного итератора (__iter__ и __next__)"""

    def test_normal(self):
        # Оборачиваем в list(), чтобы получить данные из итератора
        result = list(FibonacchiLst(list(range(10))))
        self.assertEqual(result, [0, 1, 2, 3, 5, 8])

    def test_corner_0(self):
        result = list(FibonacchiLst(list(range(0))))
        self.assertEqual(result, [])

    def test_corner_1(self):
        result = list(FibonacchiLst(list(range(1))))
        self.assertEqual(result, [0])

    def test_corner_2(self):
        result = list(FibonacchiLst(list(range(2))))
        self.assertEqual(result, [0, 1])

    def test_corner_3(self):
        result = list(FibonacchiLst([1, 1]))
        self.assertEqual(result, [1, 1])


class TestFibIteratorGetItem(unittest.TestCase):
    """Тесты для упрощенного итератора (__getitem__)"""

    def test_normal(self):
        result = list(FibonacchiLstGetItem(list(range(10))))
        self.assertEqual(result, [0, 1, 2, 3, 5, 8])

    def test_corner_0(self):
        result = list(FibonacchiLstGetItem(list(range(0))))
        self.assertEqual(result, [])

    def test_corner_1(self):
        result = list(FibonacchiLstGetItem(list(range(1))))
        self.assertEqual(result, [0])

    def test_corner_2(self):
        result = list(FibonacchiLstGetItem(list(range(2))))
        self.assertEqual(result, [0, 1])

    def test_corner_3(self):
        result = list(FibonacchiLstGetItem([1, 1]))
        self.assertEqual(result, [1, 1])

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
