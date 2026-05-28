# Решение задачи деления с использованием конфигурационного файла

## Цель работы

Разработать программу на языке Python, которая:

1. Выполняет деление двух чисел с заданной точностью.
2. Загружает значение точности из конфигурационного файла.
3. Выполняет обработку ошибок через исключения.
4. Использует модульное тестирование для проверки корректности работы.

---

## Постановка задачи

### Задание

1. Написать функцию `calculate`, которая:

   * принимает два операнда и параметр точности `epsilon`;
   * выполняет деление первого операнда на второй;
   * бросает `ZeroDivisionError` при делении на ноль;
   * бросает `ValueError` если `epsilon` вне допустимого диапазона.

   Допустимый диапазон значений:

   ```text
   10^-9 < epsilon < 10^-1
   ```

2. Написать функцию `load_params`, которая:

   * считывает значение `epsilon` из файла `settings.ini`;
   * бросает `FileNotFoundError` если файл не найден;
   * бросает `KeyError` если отсутствует секция или ключ;
   * бросает `ValueError` если значение epsilon не является числом.

3. Реализовать тестирование:

   Для функции `calculate`:

   * деление 1/2 и 1/1000;
   * деление на ноль;
   * epsilon вне допустимого диапазона.

   Для функции `load_params`:

   * успешное чтение из файла;
   * отсутствие файла;
   * неверный формат числа;
   * отсутствие секции.

---

## Описание решения

Программа состоит из следующих частей:

1. Функция `calculate` — выполняет деление с проверкой входных данных.
2. Функция `load_params` — загружает параметры из конфигурационного файла.
3. Конфигурационный файл `settings.ini` — хранит значение `epsilon`.
4. Набор модульных тестов `test_app.py`.

---

## Листинг программы

### Файл `main.py`

```python
import configparser
import os

def calculate(operand1, operand2, epsilon=0.0001):
    """
    Делит операнд 1 на операнд 2.
    Проверяет диапазон epsilon: (1e-9 < epsilon < 0.1).
    """
    # 1e-9 это 10^-9, 0.1 это 10^-1
    if not (1e-9 < epsilon < 0.1):
        raise ValueError("Точность (epsilon) вне допустимого диапазона (1e-9, 1e-1).")

    if operand2 == 0:
        raise ZeroDivisionError("Деление на ноль невозможно.")

    return float(operand1) / float(operand2)

def load_params(config_file='settings.ini'):
    """
    Считывает значение epsilon из [Settings] в .ini файле.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Файл {config_file} не найден.")
        
    config = configparser.ConfigParser()
    config.read(config_file)
    
    try:
        return config.getfloat('Settings', 'epsilon')
    except (configparser.NoSectionError, configparser.NoOptionError):
        raise KeyError("Секция [Settings] или ключ 'epsilon' не найдены.")
    except ValueError:
        raise ValueError("Неверный формат числа в файле конфигурации.")
```

---

### Конфигурационный файл `settings.ini`

```ini
[Settings]
epsilon = 0.00005
```

---

### Файл `test_app.py`

```python
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
```

---

## Результаты тестирования

В ходе тестирования были проверены следующие сценарии:

| № | Тест | Проверка | Результат |
|---|------|----------|-----------|
| 1 | `test_division_cases` | Деление 1/2 и 1/1000 | ✅ OK |
| 2 | `test_division_by_zero` | Деление на ноль → `ZeroDivisionError` | ✅ OK |
| 3 | `test_epsilon_boundaries` | Epsilon вне диапазона → `ValueError` | ✅ OK |
| 4 | `test_load_params_success` | Успешное чтение epsilon из файла | ✅ OK |
| 5 | `test_file_not_found` | Файл не найден → `FileNotFoundError` | ✅ OK |
| 6 | `test_bad_format` | Нечисловой epsilon → `ValueError` | ✅ OK |
| 7 | `test_missing_data` | Нет секции `[Settings]` → `KeyError` | ✅ OK |

```
Ran 7 tests in 0.002s

OK
```

---

## Используемые библиотеки

| Библиотека | Назначение |
|---|---|
| `configparser` | Работа с `.ini`-файлами |
| `os` | Проверка существования файла |
| `unittest` | Модульное тестирование |

---

## Структура файлов

```
├── main.py            # Основные функции
├── settings.ini       # Конфигурационный файл с epsilon
└── test_app.py        # Модульные тесты
```

---

## Вывод

В ходе выполнения работы была разработана программа для деления чисел с параметром точности `epsilon`, загружаемым из конфигурационного файла `settings.ini`.

В программе реализованы:

* деление с проверкой входных данных;
* корректная обработка ошибок через исключения (`ValueError`, `ZeroDivisionError`, `FileNotFoundError`, `KeyError`);
* загрузка параметров из `.ini`-файла;
* 7 модульных тестов, покрывающих основные и граничные случаи.

Программа успешно выполняет поставленные задачи и корректно обрабатывает исключительные ситуации.
