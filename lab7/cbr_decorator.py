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
    
    # Исходный компонент
    base_cbr = CBRComponent()
    
    # Декоратор YAML
    yaml_format = YAMLDecorator(base_cbr)
    yaml_format.save_to_file("currencies.yaml")
    print("Сохранили в currencies.yaml")
    
    # Декоратор CSV
    csv_format = CSVDecorator(base_cbr)
    csv_format.save_to_file("currencies.csv")
    print("Сохранили в currencies.csv")
