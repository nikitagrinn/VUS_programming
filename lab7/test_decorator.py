"""Тесты для декораторов ЦБ РФ."""

import os
import unittest
from unittest.mock import patch, MagicMock

from cbr_decorator import CBRComponent, YAMLDecorator, CSVDecorator, Component


# Заглушка для ответа API, чтобы не делать реальные запросы в тестах
FAKE_JSON = """
{
    "Date": "2023-10-25T11:30:00+03:00",
    "Valute": {
        "USD": {
            "ID": "R01235",
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 93.12,
            "Previous": 92.12
        }
    }
}
"""

class TestCBRComponent(unittest.TestCase):
    
    @patch('urllib.request.urlopen')
    def test_operation_returns_string(self, mock_urlopen):
        """Проверяем, что базовый компонент возвращает строку."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = FAKE_JSON.encode('utf-8')
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp
        
        comp = CBRComponent()
        result = comp.operation()
        
        self.assertIsInstance(result, str)
        self.assertIn("Доллар США", result)

    @patch('urllib.request.urlopen')
    def test_correct_url_call(self, mock_urlopen):
        """Проверка URL, по которому идет запрос."""
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{}'
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp
        
        comp = CBRComponent(url="http://test.url")
        comp.operation()
        
        mock_urlopen.assert_called_once_with("http://test.url")


class TestYAMLDecorator(unittest.TestCase):

    def setUp(self):
        self.mock_base = MagicMock(spec=Component)
        self.mock_base.operation.return_value = FAKE_JSON
        self.decorator = YAMLDecorator(self.mock_base)

    def test_yaml_conversion(self):
        """Проверка правильности конвертации в yaml."""
        result = self.decorator.operation()
        self.assertIn("Доллар США", result)
        self.assertIn("Valute:", result)
        self.assertNotIn("{", result) 

    def test_yaml_file_saving(self):
        """Проверка создания yaml файла."""
        filename = "test_data.yaml"
        self.decorator.save_to_file(filename)
        
        self.assertTrue(os.path.exists(filename))
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("USD", content)
            
        os.remove(filename)


class TestCSVDecorator(unittest.TestCase):

    def setUp(self):
        self.mock_base = MagicMock(spec=Component)
        self.mock_base.operation.return_value = FAKE_JSON
        self.decorator = CSVDecorator(self.mock_base)

    def test_csv_conversion(self):
        """Проверка правильности конвертации в csv."""
        result = self.decorator.operation()
        
        self.assertIn("ID,NumCode,CharCode,Nominal,Name,Value,Previous", result)
        self.assertIn("R01235,840,USD,1,Доллар США,93.12,92.12", result)

    def test_csv_file_saving(self):
        """Проверка создания csv файла."""
        filename = "test_data.csv"
        self.decorator.save_to_file(filename)
        
        self.assertTrue(os.path.exists(filename))
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            
        os.remove(filename)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
