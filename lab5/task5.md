# Реализация итераторов и сопрограммы для ряда Фибоначчи

## Цель работы

Изучить механизмы итерации, генераторов и сопрограмм в языке Python.

В рамках работы необходимо:

* реализовать итератор чисел Фибоначчи двумя способами;
* реализовать сопрограмму для генерации чисел Фибоначчи;
* использовать аннотацию типов;
* оформить документацию в формате PEP-257;
* разработать тесты (`unittest` и `pytest`-стиль).

---

## Постановка задачи

### Задание 1 — Сопрограмма

На основе шаблона `gen_fib.py` разработать сопрограмму, возвращающую список элементов ряда Фибоначчи по заданному `n`:

```
>> gen = my_genn()
>> gen.send(3)  →  [0, 1, 1]
>> gen.send(5)  →  [0, 1, 1, 2, 3]
>> gen.send(8)  →  [0, 1, 1, 2, 3, 5, 8, 13]
```

### Задание 2 — Итераторы

Реализовать класс `FibonacchiLst` двумя способами:

* «упрощённый» — через `__getitem__`;
* «обычный» — через `__iter__` и `__next__`.

Итератор принимает список чисел и возвращает только те, которые принадлежат ряду Фибоначчи:

```
FibonacchiLst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1])  →  [0, 1, 2, 3, 5, 8, 1]
```

---

## Теоретические сведения

### Итератор

Итератор — объект, реализующий протокол итерации: методы `__iter__` и `__next__`.

* `__iter__` возвращает сам объект;
* `__next__` возвращает следующий элемент или вызывает `StopIteration`.

Упрощённый вариант — реализация только `__getitem__`. Python автоматически создаёт итератор, перебирая индексы от 0 до `IndexError`.

### Генератор

Генератор — функция с оператором `yield`. Позволяет создавать последовательности лениво, не храня все элементы в памяти.

### Сопрограмма

Сопрограмма — расширение генератора. Главное отличие:

* генератор только **возвращает** значения через `yield`;
* сопрограмма может **получать** данные через `send()` и **возвращать** результат.

Перед первым `send(value)` сопрограмму нужно «запустить» через `send(None)` или `next()`. Для автоматизации используется декоратор priming.

---

## Описание решения

Программа состоит из двух модулей:

| Файл | Назначение |
|---|---|
| `fib_iterator.py` | Два класса-итератора (`__iter__`/`__next__` и `__getitem__`) |
| `gen_fib.py` | Бесконечный генератор и сопрограмма |
| `test_fib_it.py` | Тесты итераторов (`unittest`) |
| `test_fib.py` | Тесты сопрограммы (`pytest`-стиль) |

---

## Листинг программы

### Файл `fib_iterator.py`

```python
"""Модуль с итераторами чисел Фибоначчи."""

from typing import Iterable, List


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
```

---

### Файл `gen_fib.py`

```python
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
        gen.send(None)  # Запускаем сопрограмму до первого yield
        return gen
    return inner


@fib_coroutine
def my_genn() -> Generator[List[int], int, None]:
    """
    Сопрограмма, возвращающая список из n чисел Фибоначчи.

    Ожидает получение числа n через метод send(n).
    """
    n = yield []  # Первичное ожидание после send(None)

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
```

---

## Принцип работы сопрограммы

`fib_coroutine` — декоратор, который автоматически делает первый `send(None)`, чтобы сопрограмма дошла до первого `yield`. После этого можно сразу вызывать `send(n)`:

```python
gen = my_genn()       # декоратор уже сделал send(None)
gen.send(3)           # → [0, 1, 1]
gen.send(5)           # → [0, 1, 1, 2, 3]
```

Внутри используется `itertools.islice(fib_elem_gen(), n)` — берём ровно `n` элементов из бесконечного генератора `fib_elem_gen()`.

---

## Тестирование программы

### Файл `test_fib_it.py` — тесты итераторов

```python
"""Тесты для классов-итераторов."""

import unittest
from fib_iterator import FibonacchiLst, FibonacchiLstGetItem


class TestFibIterator(unittest.TestCase):
    """Тесты для обычного итератора (__iter__ и __next__)"""

    def test_normal(self):
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
```

---

### Файл `test_fib.py` — тесты сопрограммы

```python
"""Тесты для генератора и сопрограммы."""

from gen_fib import my_genn


def test_fib_1():
    """Тривиальный случай n = 3, список [0, 1, 1]"""
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1]


def test_fib_2():
    """Пять первых членов ряда"""
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3]


def test_fib_edge_zero():
    """Генерация при n = 0"""
    gen = my_genn()
    assert gen.send(0) == []


def test_fib_edge_negative():
    """Генерация при отрицательном количестве"""
    gen = my_genn()
    assert gen.send(-2) == []


def test_fib_multiple_sends():
    """Проверка, что сопрограмма корректно работает при серии вызовов."""
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1]
    assert gen.send(4) == [0, 1, 1, 2]
    assert gen.send(1) == [0]
```

---

## Результаты тестирования

### Итераторы (`test_fib_it.py`)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_normal` (`FibonacchiLst`) | `range(10)` → `[0,1,2,3,5,8]` | ✅ OK |
| 2 | `test_corner_0` | Пустой список → `[]` | ✅ OK |
| 3 | `test_corner_1` | `range(1)` → `[0]` | ✅ OK |
| 4 | `test_corner_2` | `range(2)` → `[0, 1]` | ✅ OK |
| 5 | `test_corner_3` | `[1, 1]` → `[1, 1]` | ✅ OK |
| 6 | `test_normal` (`FibonacchiLstGetItem`) | `range(10)` → `[0,1,2,3,5,8]` | ✅ OK |
| 7 | `test_corner_0` | Пустой список → `[]` | ✅ OK |
| 8 | `test_corner_1` | `range(1)` → `[0]` | ✅ OK |
| 9 | `test_corner_2` | `range(2)` → `[0, 1]` | ✅ OK |
| 10 | `test_corner_3` | `[1, 1]` → `[1, 1]` | ✅ OK |

```
Ran 10 tests in 0.000s

OK
```

### Сопрограмма (`test_fib.py`)

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_fib_1` | `send(3)` → `[0, 1, 1]` | ✅ OK |
| 2 | `test_fib_2` | `send(5)` → `[0, 1, 1, 2, 3]` | ✅ OK |
| 3 | `test_fib_edge_zero` | `send(0)` → `[]` | ✅ OK |
| 4 | `test_fib_edge_negative` | `send(-2)` → `[]` | ✅ OK |
| 5 | `test_fib_multiple_sends` | Серия `send()` на одном объекте | ✅ OK |

```
Ran 5 tests, 5 passed
```

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `typing` | Аннотации типов (`Iterable`, `List`, `Generator`) |
| `functools` | Декоратор `wraps` для сохранения метаданных функции |
| `itertools` | `islice` для взятия n элементов из бесконечного генератора |
| `unittest` | Тестирование итераторов |

---

## Структура файлов

```
├── fib_iterator.py      # Классы FibonacchiLst и FibonacchiLstGetItem
├── gen_fib.py           # Генератор и сопрограмма my_genn
├── test_fib_it.py       # Тесты итераторов (unittest)
└── test_fib.py          # Тесты сопрограммы (pytest-стиль)
```

---

## Вывод

В ходе выполнения работы реализованы:

* итератор `FibonacchiLst` через `__iter__` и `__next__`;
* упрощённый итератор `FibonacchiLstGetItem` через `__getitem__`;
* вспомогательная функция `is_fibonacci_number` для проверки принадлежности числа ряду;
* бесконечный генератор `fib_elem_gen` через `yield`;
* сопрограмма `my_genn` с декоратором priming `fib_coroutine`;
* 10 тестов для итераторов и 5 тестов для сопрограммы.

Весь код снабжён аннотациями типов и docstring в формате PEP-257.
