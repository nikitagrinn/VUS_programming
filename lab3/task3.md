# Разработка программы построения бинарного дерева

## Цель работы

Разработать программу на языке Python для рекурсивного построения бинарного дерева с заданными параметрами.

Также необходимо:

* реализовать отображение дерева в виде вложенных словарей;
* реализовать альтернативный вариант с использованием `collections.namedtuple`;
* разработать модульные тесты с использованием библиотеки `unittest`.

---

## Постановка задачи

Необходимо реализовать функцию:

```python
def gen_bin_tree(height=4, root=7, left_branch=..., right_branch=...):
    pass
```

Функция должна строить бинарное дерево по следующим условиям:

* в корне дерева находится число `root`;
* высота дерева задаётся параметром `height`;
* левый и правый потомки вычисляются через функции высшего порядка (lambda).

Параметры по умолчанию (Вариант №7):

```text
root = 7
height = 4
left_branch  = lambda x: x * 3
right_branch = lambda x: x - 4
```

Допустимый диапазон высоты: `height >= 0`. При `height < 0` функция возвращает `None`.

Построение дерева реализовано рекурсивно.

---

## Описание алгоритма

Алгоритм работы функции `gen_bin_tree`:

1. Если `height < 0` — вернуть `None`.
2. Если `height == 0` — вернуть листовой узел `{str(root): []}`.
3. Вычислить значения левого и правого потомков через переданные функции.
4. Рекурсивно построить левое и правое поддеревья с уменьшенной высотой.
5. Вернуть узел вида `{str(root): [left_tree, right_tree]}`.

Каждый узел дерева содержит:

* ключ — строковое представление значения (`str(root)`);
* значение — список из двух поддеревьев (или пустой список для листа).

---

## Листинг программы

### Файл `binary_tree.py`

```python
"""
Модуль для генерации бинарных деревьев.

Содержит реализацию построения бинарного дерева с использованием
вложенных словарей (базовый вариант) и с использованием namedtuple
из модуля collections (альтернативный контейнер).
"""

from typing import Dict, List, Any, Optional, Callable
from collections import namedtuple

# Определяем структуру узла для альтернативного варианта через collections
Node = namedtuple('Node', ['value', 'left', 'right'])

def gen_bin_tree(
    height: int = 4,
    root: int = 7,
    left_branch: Callable[[int], int] = lambda x: x * 3,
    right_branch: Callable[[int], int] = lambda x: x - 4
) -> Optional[Dict[str, List[Any]]]:
    """
    Рекурсивно генерирует бинарное дерево в виде вложенных словарей.
    
    Использует функции высшего порядка для вычисления значений потомков.
    По умолчанию используются параметры Варианта №7.

    Args:
        height (int): Высота дерева. Дерево с высотой 0 имеет только корень.
        root (int): Значение в корневом узле.
        left_branch (Callable): Функция для вычисления левого потомка.
        right_branch (Callable): Функция для вычисления правого потомка.

    Returns:
        Optional[Dict[str, List[Any]]]: Словарь, представляющий дерево,
        или None при некорректной (отрицательной) высоте.
    """
    if height < 0:
        return None

    # Базовый случай: достигли листьев (высота 0)
    if height == 0:
        return {str(root): []}

    # Вычисляем значения потомков с помощью переданных функций (lambda)
    left_val = left_branch(root)
    right_val = right_branch(root)

    # Рекурсивный вызов для построения поддеревьев
    return {
        str(root): [
            gen_bin_tree(height - 1, left_val, left_branch, right_branch),
            gen_bin_tree(height - 1, right_val, left_branch, right_branch)
        ]
    }


def gen_bin_tree_collections(
    height: int = 4,
    root: int = 7,
    left_branch: Callable[[int], int] = lambda x: x * 3,
    right_branch: Callable[[int], int] = lambda x: x - 4
) -> Optional[Node]:
    """
    Генерирует бинарное дерево, используя collections.namedtuple.
    """
    if height < 0:
        return None
    if height == 0:
        return Node(value=root, left=None, right=None)

    left_val = left_branch(root)
    right_val = right_branch(root)

    return Node(
        value=root,
        left=gen_bin_tree_collections(height - 1, left_val, left_branch, right_branch),
        right=gen_bin_tree_collections(height - 1, right_val, left_branch, right_branch)
    )


if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    
    print("=== Базовый вариант (Словари) ===")
    tree_dict = gen_bin_tree()
    pp.pprint(tree_dict)

    print("\n=== Вариант с collections.namedtuple ===")
    tree_namedtuple = gen_bin_tree_collections(height=2)
    print(tree_namedtuple)
```

---

## Представление дерева

### Вариант 1 — вложенные словари

Пример для `height=1`, `root=7`:

```python
{
    '7': [
        {'21': []},   # left: 7 * 3 = 21
        {'3': []}     # right: 7 - 4 = 3
    ]
}
```

### Вариант 2 — `collections.namedtuple`

```python
Node(value=7,
     left=Node(value=21, left=None, right=None),
     right=Node(value=3, left=None, right=None))
```

---

## Тестирование программы

### Файл `test_binary_tree.py`

```python
"""
Тесты для функций генерации бинарного дерева.
"""

import unittest
from binary_tree import gen_bin_tree, gen_bin_tree_collections, Node

class TestGenBinTree(unittest.TestCase):
    """Набор тестов для проверки функции gen_bin_tree (словари)."""

    def test_default_variant_height_0(self):
        """Тестирование генерации дерева высотой 0 по умолчанию (Вар. 7)."""
        self.assertEqual(gen_bin_tree(height=0), {'7': []})

    def test_default_variant_height_1(self):
        """Тестирование генерации дерева высотой 1 по умолчанию (Вар. 7)."""
        expected = {
            '7': [
                {'21': []},
                {'3': []}
            ]
        }
        self.assertEqual(gen_bin_tree(height=1), expected)

    def test_default_variant_height_2(self):
        """Тестирование генерации дерева высотой 2 по умолчанию (Вар. 7)."""
        expected = {
            '7': [
                {'21': [{'63': []}, {'17': []}]},
                {'3': [{'9': []}, {'-1': []}]}
            ]
        }
        self.assertEqual(gen_bin_tree(height=2), expected)

    def test_custom_parameters(self):
        """Тестирование с передачей пользовательских параметров."""
        expected = {
            '13': [
                {'14': []},
                {'12': []}
            ]
        }
        result = gen_bin_tree(
            height=1,
            root=13,
            left_branch=lambda x: x + 1,
            right_branch=lambda x: x - 1
        )
        self.assertEqual(result, expected)
    
    def test_negative_height(self):
        """Тестирование с отрицательной высотой."""
        self.assertIsNone(gen_bin_tree(height=-1))

class TestGenBinTreeCollections(unittest.TestCase):
    """Набор тестов для структуры на базе collections.namedtuple."""

    def test_namedtuple_height_1(self):
        """Тестирование namedtuple с высотой 1."""
        expected = Node(
            value=7,
            left=Node(value=21, left=None, right=None),
            right=Node(value=3, left=None, right=None)
        )
        self.assertEqual(gen_bin_tree_collections(height=1), expected)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
```

---

## Результаты тестирования

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_default_variant_height_0` | Дерево высотой 0 → лист `{'7': []}` | ✅ OK |
| 2 | `test_default_variant_height_1` | Дерево высотой 1, Вариант №7 | ✅ OK |
| 3 | `test_default_variant_height_2` | Дерево высотой 2, Вариант №7 | ✅ OK |
| 4 | `test_custom_parameters` | Пользовательские lambda | ✅ OK |
| 5 | `test_negative_height` | Отрицательная высота → `None` | ✅ OK |
| 6 | `test_namedtuple_height_1` | `namedtuple` высотой 1 | ✅ OK |

```
Ran 6 tests in 0.000s

OK
```

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `collections.namedtuple` | Альтернативная структура узла дерева |
| `typing` | Аннотации типов (`Callable`, `Optional`, `Dict`) |
| `pprint` | Форматированный вывод дерева |
| `unittest` | Модульное тестирование |

---

## Структура файлов

```
├── binary_tree.py        # Основной код
└── test_binary_tree.py   # Модульные тесты
```

---

## Вывод

В ходе выполнения работы была разработана программа для рекурсивного построения бинарного дерева.

В программе реализованы:

* рекурсивный алгоритм построения дерева;
* параметризованные функции ветвления через функции высшего порядка;
* два варианта хранения: вложенные словари и `collections.namedtuple`;
* аннотации типов (`Callable`, `Optional`, `Dict`);
* 6 модульных тестов, покрывающих основные случаи и оба варианта реализации.

Все поставленные задачи выполнены.
