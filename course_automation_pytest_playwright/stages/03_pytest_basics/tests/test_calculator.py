"""
test_calculator.py - Комплексные тесты для модуля calculator

Этот файл демонстрирует различные техники тестирования с pytest:
- Базовые тесты функций
- Параметризованные тесты
- Тесты с фикстурами
- Тесты исключений
- Маркированные тесты
"""

import pytest
import math
from src.calculator import (
    add, subtract, multiply, divide, power, square_root,
    factorial, is_prime, fibonacci, average, median, gcd, lcm
)


class TestBasicOperations:
    """Тесты базовых арифметических операций"""
    
    def test_addition(self):
        """Тест сложения чисел"""
        # Нормальные случаи
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
        assert add(2.5, 3.7) == 6.2
        
        # Граничные случаи
        assert add(float('inf'), 1) == float('inf')
        assert str(add(float('nan'), 1)) == 'nan'
    
    def test_subtraction(self):
        """Тест вычитания чисел"""
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
        assert subtract(-3, -2) == -1
        assert subtract(2.5, 1.3) == 1.2
    
    def test_multiplication(self):
        """Тест умножения чисел"""
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0
        assert multiply(2.5, 4) == 10.0
    
    def test_division(self):
        """Тест деления чисел"""
        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5
        assert divide(-10, 2) == -5.0
        
        # Тест деления на ноль
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            divide(10, 0)
        
        with pytest.raises(ValueError):
            divide(-5, 0)


class TestAdvancedMath:
    """Тесты продвинутых математических функций"""
    
    @pytest.mark.parametrize("base,exp,expected", [
        (2, 3, 8),
        (5, 0, 1),
        (3, 2, 9),
        (10, -1, 0.1),
        (2, 0.5, math.sqrt(2)),
    ])
    def test_power(self, base, exp, expected):
        """Параметризованный тест возведения в степень"""
        result = power(base, exp)
        if isinstance(expected, float):
            assert abs(result - expected) < 1e-10
        else:
            assert result == expected
    
    def test_square_root(self):
        """Тест квадратного корня"""
        assert square_root(4) == 2.0
        assert square_root(9) == 3.0
        assert square_root(0) == 0.0
        assert abs(square_root(2) - math.sqrt(2)) < 1e-10
        
        # Тест отрицательных чисел
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            square_root(-1)
        
        with pytest.raises(ValueError):
            square_root(-100)


class TestNumberTheory:
    """Тесты теории чисел"""
    
    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
    ])
    def test_factorial(self, n, expected):
        """Параметризованный тест факториала"""
        assert factorial(n) == expected
    
    def test_factorial_errors(self):
        """Тест ошибок факториала"""
        with pytest.raises(ValueError):
            factorial(-1)
        
        with pytest.raises(ValueError):
            factorial(3.14)
        
        with pytest.raises(ValueError):
            factorial("5")
    
    @pytest.mark.parametrize("n,expected", [
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (25, False),
        (97, True),
        (1, False),
        (0, False),
    ])
    def test_is_prime(self, n, expected):
        """Параметризованный тест простых чисел"""
        assert is_prime(n) == expected
    
    @pytest.mark.parametrize("n,expected", [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (10, 55),
    ])
    def test_fibonacci(self, n, expected):
        """Параметризованный тест чисел Фибоначчи"""
        assert fibonacci(n) == expected
    
    def test_fibonacci_errors(self):
        """Тест ошибок чисел Фибоначчи"""
        with pytest.raises(ValueError):
            fibonacci(-1)
        
        with pytest.raises(ValueError):
            fibonacci(-10)


class TestStatistics:
    """Тесты статистических функций"""
    
    def test_average(self):
        """Тест вычисления среднего"""
        assert average([1, 2, 3, 4, 5]) == 3.0
        assert average([10, 20, 30]) == 20.0
        assert average([2.5, 3.5, 4.5]) == 3.5
        assert average([0]) == 0.0
        
        # Тест пустого списка
        with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
            average([])
    
    def test_median(self):
        """Тест вычисления медианы"""
        # Нечетное количество элементов
        assert median([1, 2, 3, 4, 5]) == 3
        assert median([3, 1, 4, 1, 5]) == 3
        
        # Четное количество элементов
        assert median([1, 2, 3, 4]) == 2.5
        assert median([1, 3, 3, 7]) == 3.0
        
        # Один элемент
        assert median([42]) == 42
        
        # Тест пустого списка
        with pytest.raises(ValueError):
            median([])


class TestGCD_LCM:
    """Тесты НОД и НОК"""
    
    @pytest.mark.parametrize("a,b,expected_gcd,expected_lcm", [
        (12, 8, 4, 24),
        (17, 13, 1, 221),
        (100, 25, 25, 100),
        (0, 5, 5, 0),
        (7, 7, 7, 7),
        (-12, 8, 4, 24),  # Отрицательные числа
    ])
    def test_gcd_lcm(self, a, b, expected_gcd, expected_lcm):
        """Параметризованный тест НОД и НОК"""
        assert gcd(a, b) == expected_gcd
        assert lcm(a, b) == expected_lcm


class TestEdgeCases:
    """Тесты граничных случаев и специальных значений"""
    
    @pytest.mark.slow
    def test_large_numbers(self):
        """Тест с большими числами (медленный тест)"""
        # Большой факториал
        result = factorial(10)
        assert result == 3628800
        
        # Большое число Фибоначчи
        result = fibonacci(20)
        assert result == 6765
    
    @pytest.mark.xfail(reason="Float precision issues")
    def test_float_precision_edge_case(self):
        """Тест, который ожидаемо падает из-за точности float"""
        result = add(0.1, 0.2)
        assert result == 0.3  # Это упадет из-за особенностей float
    
    @pytest.mark.skip(reason="Not implemented yet")
    def test_complex_numbers_support(self):
        """Тест для будущей поддержки комплексных чисел"""
        # Этот тест будет пропущен
        pass


# Маркированные тесты для выборочного запуска
@pytest.mark.fast
def test_quick_operations():
    """Быстрые тесты для CI"""
    assert add(1, 1) == 2
    assert multiply(2, 3) == 6
    assert is_prime(7) == True


@pytest.mark.slow
def test_comprehensive_prime_check():
    """Комплексная проверка простых чисел (медленный тест)"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for prime in primes:
        assert is_prime(prime) == True
    
    non_primes = [0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
    for non_prime in non_primes:
        assert is_prime(non_prime) == False


# Тесты с параметризацией и несколькими аргументами
@pytest.mark.parametrize("operation,a,b,expected", [
    (add, 2, 3, 5),
    (subtract, 5, 3, 2),
    (multiply, 4, 5, 20),
    (divide, 10, 2, 5.0),
])
def test_arithmetic_operations(operation, a, b, expected):
    """Параметризованный тест арифметических операций"""
    if operation == divide and b == 0:
        with pytest.raises(ValueError):
            operation(a, b)
    else:
        result = operation(a, b)
        if isinstance(expected, float):
            assert abs(result - expected) < 1e-10
        else:
            assert result == expected


if __name__ == "__main__":
    # Можно запустить тесты напрямую
    pytest.main([__file__, "-v"])