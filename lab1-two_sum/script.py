import unittest

class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in seen:
                return [seen[diff], i]
            seen[num] = i
        return []

class TestTwoSum(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_basic_cases(self):
        self.assertEqual(self.solution.two_sum([2, 7, 11, 15], 9), [0, 1])
        self.assertEqual(self.solution.two_sum([3, 2, 4], 6), [1, 2])
        self.assertEqual(self.solution.two_sum([3, 3], 6), [0, 1])

    def test_custom_data(self):
        self.assertEqual(self.solution.two_sum([16, 2, 15, 89], 105), [0, 3])

    def test_negative_numbers(self):
        self.assertEqual(self.solution.two_sum([-1, -2, -3, -4, -5], -8), [2, 4])

    def test_zero_target(self):
        self.assertEqual(self.solution.two_sum([1, -1, 2, 3], 0), [0, 1])

    def test_no_solution(self):
        self.assertEqual(self.solution.two_sum([1, 2, 3, 4], 10), [])

    def test_duplicate_numbers(self):
        self.assertEqual(self.solution.two_sum([3, 3, 4, 5], 6), [0, 1])


if __name__ == '__main__':
    unittest.main()
