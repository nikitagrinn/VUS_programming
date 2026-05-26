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
