"""Тесты для генератора и сопрограммы."""

from gen_fib import my_genn

def test_fib_1():
    """Тривиальный случай n = 3, список [0, 1, 1]"""
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1]

def test_fib_2():
    """Пять первых членов ряда"""
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3]

def test_fib_edge_zero():
    """Генерация при n = 0"""
    gen = my_genn()
    assert gen.send(0) == []

def test_fib_edge_negative():
    """Генерация при отрицательном количестве"""
    gen = my_genn()
    assert gen.send(-2) == []

def test_fib_multiple_sends():
    """Проверка, что сопрограмма не 'забывает' свое состояние при серии вызовов."""
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1]
    assert gen.send(4) == [0, 1, 1, 2]
    assert gen.send(1) == [0]
