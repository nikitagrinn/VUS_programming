import unittest

class Solution:
    """Решает задачу Two Sum за время O(n) с использованием хэш-таблицы."""

    def two_sum(self, nums, target):
        # Словарь для хранения чисел и их индексов: {число: индекс}
        seen = {}
        
        for i, num in enumerate(nums):
            # Ищем, есть ли уже в словаре число, которое в сумме с текущим даст target
            complement = target - num
            
            if complement in seen:
                # Если нашли, возвращаем индекс найденного числа и текущий индекс
                return [seen[complement], i]
            
            # Если не нашли, добавляем текущее число и его индекс в словарь
            seen[num] = i

        return [] # На случай, если решения нет (хотя по условию оно всегда есть)


# --- Блок с Unit-тестами ---

class TestTwoSum(unittest.TestCase):
    
    def setUp(self):
        """Этот метод вызывается перед каждым тестом. Создаем экземпляр Solution."""
        self.solution = Solution()

    def test_example_1(self):
        """Пример 1 из LeetCode"""
        nums = [2, 7, 11, 15]
        target = 9
        # Ожидаем, что результат будет [0, 1]
        self.assertEqual(self.solution.two_sum(nums, target), [0, 1])

    def test_example_2(self):
        """Пример 2 из LeetCode"""
        nums = [3, 2, 4]
        target = 6
        self.assertEqual(self.solution.two_sum(nums, target), [1, 2])

    def test_example_3(self):
        """Пример 3 из LeetCode"""
        nums = [3, 3]
        target = 6
        self.assertEqual(self.solution.two_sum(nums, target), [0, 1])

    def test_custom_data(self):
        """Твой собственный пример из исходного кода"""
        nums = [16, 2, 15, 89]
        target = 105
        # 16 (индекс 0) + 89 (индекс 3) = 105
        self.assertEqual(self.solution.two_sum(nums, target), [0, 3])

    def test_negative_numbers(self):
        """Тест с отрицательными числами (ограничения LeetCode допускают минус)"""
        nums = [-1, -2, -3, -4, -5]
        target = -8
        self.assertEqual(self.solution.two_sum(nums, target), [2, 4])


if __name__ == '__main__':
    # Эта команда автоматически найдет все методы, начинающиеся на test_
    # и запустит их, выведя красивый отчет в консоль.
    unittest.main()
