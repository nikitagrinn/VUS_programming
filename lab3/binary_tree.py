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

    Args:
        height (int): Высота дерева.
        root (int): Значение в корне.
        left_branch (Callable): Функция для левого потомка.
        right_branch (Callable): Функция для правого потомка.

    Returns:
        Optional[Node]: Корневой узел дерева в виде namedtuple.
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
    # Вызов без аргументов использует вариант 7 по умолчанию
    tree_dict = gen_bin_tree() 
    pp.pprint(tree_dict)

    print("\n=== Вариант с collections.namedtuple ===")
    tree_namedtuple = gen_bin_tree_collections(height=2) # Сделаем поменьше для вывода
    print(tree_namedtuple)
