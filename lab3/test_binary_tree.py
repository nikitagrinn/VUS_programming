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
        """Тестирование с передачей пользовательских параметров (не из варианта)."""
        # Например, Вариант 13: Root = 13; height = 1, left = root+1, right = root-1
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
        # Корень 7, левый 21, правый 3
        expected = Node(
            value=7,
            left=Node(value=21, left=None, right=None),
            right=Node(value=3, left=None, right=None)
        )
        self.assertEqual(gen_bin_tree_collections(height=1), expected)


if __name__ == '__main__':
    # Эта строка позволяет запускать тесты в средах типа Google Colab
    unittest.main(argv=[''], verbosity=2, exit=False)
