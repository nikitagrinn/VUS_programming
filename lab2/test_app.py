import unittest
import os
from main import calculate, load_params

class TestLab(unittest.TestCase):
    
    def setUp(self):
        self.test_ini = 'test_settings.ini'

    def tearDown(self):
        if os.path.exists(self.test_ini):
            os.remove(self.test_ini)

    # --- Тесты для calculate ---

    def test_division_cases(self):
        """Тест 1/2 с epsilon=0.1 и 1/1000 с epsilon=0.001"""
        self.assertAlmostEqual(calculate(1, 2, epsilon=0.01), 0.5)
        self.assertAlmostEqual(calculate(1, 1000, epsilon=0.001), 0.001)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate(10, 0)

    def test_epsilon_boundaries(self):
        # Ошибка, так как epsilon слишком большой (>= 0.1)
        with self.assertRaises(ValueError):
            calculate(1, 2, epsilon=0.5)
        # Ошибка, так как epsilon слишком маленький
        with self.assertRaises(ValueError):
            calculate(1, 2, epsilon=1e-10)

    # --- Тесты для load_params ---

    def test_load_params_success(self):
        with open(self.test_ini, 'w') as f:
            f.write('[Settings]\nepsilon = 0.005\n')
        self.assertEqual(load_params(self.test_ini), 0.005)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_params('missing_file.ini')

    def test_bad_format(self):
        with open(self.test_ini, 'w') as f:
            f.write('[Settings]\nepsilon = not_a_number\n')
        with self.assertRaises(ValueError):
            load_params(self.test_ini)

    def test_missing_data(self):
        with open(self.test_ini, 'w') as f:
            f.write('[WrongSection]\nepsilon = 0.01\n')
        with self.assertRaises(KeyError):
            load_params(self.test_ini)

if __name__ == '__main__':
    unittest.main()
