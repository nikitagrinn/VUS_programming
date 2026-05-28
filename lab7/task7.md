# Паттерн «Декоратор» для работы с курсами валют ЦБ РФ

## Цель работы

Изучить применение шаблона проектирования «Декоратор» на языке Python.

В рамках работы необходимо:

* реализовать базовый компонент для получения курсов валют через API Центробанка РФ;
* реализовать декораторы для преобразования данных в YAML и CSV;
* использовать абстрактные классы и интерфейсы (`ABC`, `@abstractmethod`);
* реализовать сохранение данных в файлы;
* оформить программу в соответствии с требованиями PEP-8, PEP-257 и PEP-484;
* разработать тесты с использованием `unittest.mock`.

---

## Постановка задачи

На основе шаблона «Декоратор» реализовать:

1. Базовый компонент `CBRComponent`, который:
   * получает данные о курсах валют через API ЦБ РФ;
   * возвращает данные в формате JSON-строки.

2. Конкретные декораторы:
   * `YAMLDecorator` — конвертирует JSON в YAML и сохраняет в файл;
   * `CSVDecorator` — конвертирует данные блока `Valute` в CSV и сохраняет в файл.

Каждый декоратор должен:
* переопределять метод `operation()`;
* реализовывать метод `save_to_file(filename)`.

Источник данных:

```text
https://www.cbr-xml-daily.ru/daily_json.js
```

---

## Теоретические сведения

### Паттерн «Декоратор»

Паттерн «Декоратор» позволяет динамически расширять функциональность объектов без изменения их исходного кода. Вместо наследования используется обёртка (wrapper) — объект, который хранит ссылку на исходный компонент и добавляет новое поведение.

Основные элементы паттерна:

| Элемент | Назначение |
|---|---|
| `Component` | Абстрактный интерфейс |
| `CBRComponent` | Конкретный компонент — получает JSON с API |
| `Decorator` | Базовый декоратор — делегирует вызов компоненту |
| `YAMLDecorator` | Конкретный декоратор — конвертирует в YAML |
| `CSVDecorator` | Конкретный декоратор — конвертирует в CSV |

### Абстрактные классы

Для реализации интерфейса используется модуль `abc`. Методы, объявленные через `@abstractmethod`, обязательны к реализации в дочерних классах:

```python
class Component(abc.ABC):
    @abc.abstractmethod
    def operation(self) -> str:
        pass
```

### Тестирование с mock-объектами

Чтобы не делать реальные HTTP-запросы в тестах, используется `unittest.mock.patch` и `MagicMock`. Они подменяют `urllib.request.urlopen` заглушкой, возвращающей фиктивный JSON.

---

## Листинг программы

### Файл `cbr_decorator.py`

```python
"""Работа с API ЦБ РФ через паттерн Декоратор."""

import abc
import json
import csv
import urllib.request
from io import StringIO
from typing import Any

import yaml


class Component(abc.ABC):
    """Базовый интерфейс для компонентов."""

    @abc.abstractmethod
    def operation(self) -> str:
        """Основной метод, который будут переопределять декораторы."""
        pass


class CBRComponent(Component):
    """Класс для получения исходных данных от Центробанка в формате JSON."""

    def __init__(self, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> None:
        self._url = url

    def operation(self) -> str:
        """Делает запрос к API и возвращает строку с JSON."""
        with urllib.request.urlopen(self._url) as response:
            return response.read().decode('utf-8')


class Decorator(Component):
    """Базовый класс декоратора."""

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        return self._component

    def operation(self) -> str:
        return self._component.operation()

    @abc.abstractmethod
    def save_to_file(self, filename: str) -> None:
        """Метод для сохранения результата в файл."""
        pass


class YAMLDecorator(Decorator):
    """Декоратор для конвертации JSON в YAML."""

    def operation(self) -> str:
        """Возвращает данные в формате yaml."""
        json_data = super().operation()
        data_dict = json.loads(json_data)
        return yaml.dump(data_dict, allow_unicode=True, default_flow_style=False)

    def save_to_file(self, filename: str) -> None:
        """Записывает yaml-строку в файл."""
        yaml_data = self.operation()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(yaml_data)


class CSVDecorator(Decorator):
    """Декоратор для выгрузки валют в CSV."""

    def operation(self) -> str:
        """Парсит JSON и собирает плоскую таблицу CSV только для блока Valute."""
        json_data = super().operation()
        data_dict = json.loads(json_data)

        valutes = data_dict.get("Valute", {})
        if not valutes:
            return ""

        output = StringIO()
        headers = list(list(valutes.values())[0].keys())
        writer = csv.DictWriter(output, fieldnames=headers, lineterminator='\n')

        writer.writeheader()
        for valute_info in valutes.values():
            writer.writerow(valute_info)

        return output.getvalue()

    def save_to_file(self, filename: str) -> None:
        """Записывает csv-строку в файл."""
        csv_data = self.operation()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(csv_data)


if __name__ == "__main__":
    print("Тянем данные с ЦБ РФ...")

    base_cbr = CBRComponent()

    yaml_format = YAMLDecorator(base_cbr)
    yaml_format.save_to_file("currencies.yaml")
    print("Сохранили в currencies.yaml")

    csv_format = CSVDecorator(base_cbr)
    csv_format.save_to_file("currencies.csv")
    print("Сохранили в currencies.csv")
```

---

### Файл `requirements.txt`

```text
PyYAML==6.0.1
```

---

## Структура программы

```
Component (ABC)
    └── CBRComponent          # Получает JSON с API ЦБ РФ
    └── Decorator (ABC)       # Базовый декоратор
            ├── YAMLDecorator # JSON → YAML
            └── CSVDecorator  # JSON → CSV (все поля блока Valute)
```

Ключевое отличие от прямого наследования: декоратор хранит **ссылку** на обёртываемый объект и вызывает его `operation()` через `super().operation()`. Это позволяет цеплять декораторы в цепочку.

---

## Тестирование программы

### Файл `test_decorator.py`

```python
"""Тесты для декораторов ЦБ РФ."""

import os
import unittest
from unittest.mock import patch, MagicMock

from cbr_decorator import CBRComponent, YAMLDecorator, CSVDecorator, Component


# Заглушка для ответа API — реальные запросы в тестах не делаются
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
            self.assertEqual(len(lines), 2)  # заголовок + 1 запись

        os.remove(filename)


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
```

---

## Результаты тестирования

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_operation_returns_string` | `CBRComponent.operation()` возвращает строку с данными | ✅ OK |
| 2 | `test_correct_url_call` | Запрос идёт по заданному URL | ✅ OK |
| 3 | `test_yaml_conversion` | JSON корректно конвертируется в YAML-строку | ✅ OK |
| 4 | `test_yaml_file_saving` | YAML-файл создаётся и содержит данные | ✅ OK |
| 5 | `test_csv_conversion` | CSV содержит заголовок и строку данных | ✅ OK |
| 6 | `test_csv_file_saving` | CSV-файл создаётся, содержит 2 строки | ✅ OK |

```
Ran 6 tests in 0.004s

OK
```

> Тесты используют `unittest.mock.patch` и `MagicMock` — реальные HTTP-запросы не выполняются, что делает тесты быстрыми и не зависящими от сети.

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `abc` | Реализация абстрактных классов и интерфейсов |
| `json` | Парсинг JSON-ответа от API |
| `csv` | Формирование CSV через `DictWriter` |
| `urllib.request` | HTTP-запросы (без внешних зависимостей) |
| `PyYAML` | Конвертация в YAML-формат |
| `typing` | Аннотации типов |
| `unittest.mock` | Mock-объекты для тестирования без сети |

---

## Структура файлов

```
├── cbr_decorator.py     # Основной код (Component, декораторы)
├── test_decorator.py    # Модульные тесты с mock
└── requirements.txt     # Зависимости (PyYAML==6.0.1)
```

---

## Вывод

В ходе выполнения работы реализован шаблон проектирования «Декоратор».

В программе реализованы:

* абстрактный интерфейс `Component` через `ABC` и `@abstractmethod`;
* базовый компонент `CBRComponent` для получения JSON с API ЦБ РФ через `urllib`;
* базовый декоратор `Decorator` с делегированием вызовов;
* `YAMLDecorator` — конвертирует JSON в YAML и сохраняет в файл;
* `CSVDecorator` — конвертирует блок `Valute` в полноценный CSV (все поля) через `csv.DictWriter`;
* 6 модульных тестов с `unittest.mock` — без реальных HTTP-запросов.

Код соответствует требованиям PEP-8, PEP-257 и PEP-484.
