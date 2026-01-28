"""
calculator.py - Пример модуля для тестирования

Этот модуль содержит различные функции для демонстрации
тестирования с pytest, включая нормальные случаи, граничные условия
и обработку ошибок.
"""

import math
from typing import List, Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Сложение двух чисел
    
    Args:
        a: Первое число
        b: Второе число
    
    Returns:
        Сумма чисел a и b
    
    Examples:
        >>> add(2, 3)
        5
        >>> add(-1, 1)
        0
        >>> add(2.5, 3.7)
        6.2
    """
    return a + b


def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Вычитание двух чисел
    
    Args:
        a: Уменьшаемое
        b: Вычитаемое
    
    Returns:
        Разность чисел a и b
    """
    return a - b


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Умножение двух чисел
    
    Args:
        a: Первый множитель
        b: Второй множитель
    
    Returns:
        Произведение чисел a и b
    """
    return a * b


def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Деление двух чисел
    
    Args:
        a: Делимое
        b: Делитель
    
    Returns:
        Частное от деления a на b
    
    Raises:
        ValueError: Если делитель равен нулю
    
    Examples:
        >>> divide(10, 2)
        5.0
        >>> divide(7, 2)
        3.5
        >>> divide(10, 0)
        Traceback (most recent call last):
        ...
        ValueError: Division by zero is not allowed
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b


def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """
    Возведение числа в степень
    
    Args:
        base: Основание
        exponent: Показатель степени
    
    Returns:
        base в степени exponent
    """
    return base ** exponent


def square_root(number: Union[int, float]) -> float:
    """
    Квадратный корень числа
    
    Args:
        number: Число для извлечения корня
    
    Returns:
        Квадратный корень числа
    
    Raises:
        ValueError: Если число отрицательное
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(number)


def factorial(n: int) -> int:
    """
    Факториал числа
    
    Args:
        n: Неотрицательное целое число
    
    Returns:
        Факториал числа n
    
    Raises:
        ValueError: Если n отрицательное или не целое
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial is only defined for non-negative integers")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_prime(n: int) -> bool:
    """
    Проверка, является ли число простым
    
    Args:
        n: Целое число для проверки
    
    Returns:
        True если число простое, False в противном случае
    
    Examples:
        >>> is_prime(2)
        True
        >>> is_prime(17)
        True
        >>> is_prime(4)
        False
        >>> is_prime(1)
        False
    """
    if n < 2:
        return False
    
    if n == 2:
        return True
    
    if n % 2 == 0:
        return False
    
    # Проверяем делители до sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    
    return True


def fibonacci(n: int) -> int:
    """
    N-ое число Фибоначчи
    
    Args:
        n: Номер числа в последовательности (0-indexed)
    
    Returns:
        N-ое число Фибоначчи
    
    Raises:
        ValueError: Если n отрицательное
    
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(5)
        5
        >>> fibonacci(10)
        55
    """
    if n < 0:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def average(numbers: List[Union[int, float]]) -> float:
    """
    Вычисление среднего значения списка чисел
    
    Args:
        numbers: Список чисел
    
    Returns:
        Среднее значение
    
    Raises:
        ValueError: Если список пуст
    
    Examples:
        >>> average([1, 2, 3, 4, 5])
        3.0
        >>> average([10, 20, 30])
        20.0
        >>> average([])
        Traceback (most recent call last):
        ...
        ValueError: Cannot calculate average of empty list
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    return sum(numbers) / len(numbers)


def median(numbers: List[Union[int, float]]) -> float:
    """
    Медиана списка чисел
    
    Args:
        numbers: Список чисел
    
    Returns:
        Медиана списка
    
    Raises:
        ValueError: Если список пуст
    
    Examples:
        >>> median([1, 2, 3, 4, 5])
        3
        >>> median([1, 2, 3, 4])
        2.5
        >>> median([5])
        5
    """
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    if n % 2 == 1:
        # Нечетное количество элементов
        return sorted_numbers[n // 2]
    else:
        # Четное количество элементов
        mid1 = sorted_numbers[n // 2 - 1]
        mid2 = sorted_numbers[n // 2]
        return (mid1 + mid2) / 2


def gcd(a: int, b: int) -> int:
    """
    Наибольший общий делитель двух чисел
    
    Args:
        a: Первое число
        b: Второе число
    
    Returns:
        НОД чисел a и b
    
    Examples:
        >>> gcd(12, 8)
        4
        >>> gcd(17, 13)
        1
        >>> gcd(0, 5)
        5
    """
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """
    Наименьшее общее кратное двух чисел
    
    Args:
        a: Первое число
        b: Второе число
    
    Returns:
        НОК чисел a и b
    
    Examples:
        >>> lcm(12, 8)
        24
        >>> lcm(7, 5)
        35
        >>> lcm(0, 5)
        0
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


# Для тестирования doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)