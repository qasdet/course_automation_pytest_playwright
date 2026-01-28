"""
🧪 Шаблоны тестов для автоматизации

Этот файл содержит готовые шаблоны для различных типов тестов,
которые можно использовать как основу для написания собственных тестов.
"""

# =============================================================================
# БАЗОВЫЙ ШАБЛОН ТЕСТА С PYTEST
# =============================================================================

import pytest

def test_basic_example():
    """Базовый шаблон теста"""
    # ARRANGE - Подготовка данных
    expected_result = 42
    input_data = 10
    
    # ACT - Выполнение действия
    actual_result = input_data * 4.2
    
    # ASSERT - Проверка результата
    assert actual_result == expected_result, f"Ожидалось {expected_result}, получено {actual_result}"

# =============================================================================
# ШАБЛОН ПАРАМЕТРИЗОВАННОГО ТЕСТА
# =============================================================================

@pytest.mark.parametrize("input_value,expected_output", [
    (2, 4),
    (3, 9),
    (0, 0),
    (-2, 4),
])
def test_square_function(input_value, expected_output):
    """Тест квадратной функции с разными параметрами"""
    def square(x):
        return x * x
    
    result = square(input_value)
    assert result == expected_output

# =============================================================================
# ШАБЛОН ТЕСТА С FIXTURE
# =============================================================================

@pytest.fixture
def sample_data():
    """Fixture для подготовки тестовых данных"""
    return {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "settings": {
            "timeout": 30,
            "retry_count": 3
        }
    }

def test_user_processing(sample_data):
    """Тест обработки пользовательских данных"""
    users = sample_data["users"]
    assert len(users) == 2
    assert users[0]["name"] == "Alice"

# =============================================================================
# ШАБЛОН ТЕСТА API
# =============================================================================

import requests

def test_api_get_request():
    """Тест GET запроса к API"""
    # ARRANGE
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/posts/1"
    
    # ACT
    response = requests.get(base_url + endpoint)
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "userId" in data

def test_api_post_request():
    """Тест POST запроса к API"""
    # ARRANGE
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/posts"
    payload = {
        "title": "Test Post",
        "body": "This is a test post",
        "userId": 1
    }
    
    # ACT
    response = requests.post(base_url + endpoint, json=payload)
    
    # ASSERT
    assert response.status_code == 201
    created_post = response.json()
    assert created_post["title"] == payload["title"]
    assert "id" in created_post

# =============================================================================
# ШАБЛОН ТЕСТА С ИСКЛЮЧЕНИЯМИ
# =============================================================================

def test_exception_handling():
    """Тест обработки исключений"""
    
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль")
        return a / b
    
    # Тест нормального случая
    assert divide(10, 2) == 5
    
    # Тест исключения
    with pytest.raises(ZeroDivisionError) as exc_info:
        divide(10, 0)
    
    assert "Деление на ноль" in str(exc_info.value)

# =============================================================================
# ШАБЛОН ТЕСТА С MOCK
# =============================================================================

from unittest.mock import Mock, patch

def test_with_mock():
    """Тест с использованием mock объектов"""
    
    # Создание mock объекта
    mock_service = Mock()
    mock_service.get_user.return_value = {"id": 1, "name": "Test User"}
    
    # Использование mock
    user = mock_service.get_user(1)
    
    # Проверки
    assert user["name"] == "Test User"
    mock_service.get_user.assert_called_once_with(1)

# =============================================================================
# ШАБЛОН ТЕСТА ПРОИЗВОДИТЕЛЬНОСТИ
# =============================================================================

import time

def test_performance_basic():
    """Базовый тест производительности"""
    
    def slow_function():
        time.sleep(0.1)  # Имитация медленной операции
        return "done"
    
    start_time = time.time()
    result = slow_function()
    end_time = time.time()
    
    execution_time = end_time - start_time
    assert result == "done"
    assert execution_time < 1.0, f"Функция выполнялась слишком долго: {execution_time} секунд"

# =============================================================================
# ШАБЛОН ТЕСТА СЛОЖНОЙ ЛОГИКИ
# =============================================================================

class TestUserAuthentication:
    """Класс для тестирования аутентификации пользователей"""
    
    def setup_method(self):
        """Подготовка перед каждым тестом"""
        self.auth_service = AuthService()
        self.valid_credentials = {"username": "testuser", "password": "password123"}
    
    def test_valid_login(self):
        """Тест успешной авторизации"""
        result = self.auth_service.login(
            self.valid_credentials["username"],
            self.valid_credentials["password"]
        )
        
        assert result["success"] is True
        assert "token" in result
        assert len(result["token"]) > 0
    
    def test_invalid_password(self):
        """Тест неверного пароля"""
        result = self.auth_service.login("testuser", "wrongpassword")
        assert result["success"] is False
        assert "error" in result
    
    def test_nonexistent_user(self):
        """Тест несуществующего пользователя"""
        result = self.auth_service.login("nonexistent", "password")
        assert result["success"] is False

# =============================================================================
# ШАБЛОН ТЕСТА С КОНФИГУРАЦИЕЙ
# =============================================================================

import json
import os

@pytest.fixture
def test_config():
    """Fixture для загрузки тестовой конфигурации"""
    config_path = os.path.join(os.path.dirname(__file__), "test_config.json")
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        return {
            "base_url": "https://test.example.com",
            "timeout": 30,
            "browser": "chrome"
        }

def test_config_loading(test_config):
    """Тест загрузки конфигурации"""
    assert "base_url" in test_config
    assert isinstance(test_config["timeout"], int)
    assert test_config["timeout"] > 0

# =============================================================================
# ШАБЛОН ТЕСТА С ДАННЫМИ ИЗ ФАЙЛА
# =============================================================================

import csv

@pytest.fixture
def test_data_csv():
    """Fixture для загрузки тестовых данных из CSV"""
    data = []
    csv_path = os.path.join(os.path.dirname(__file__), "test_data.csv")
    
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    
    return data

def test_data_driven_with_csv(test_data_csv):
    """Тест с данными из CSV файла"""
    if not test_data_csv:
        pytest.skip("Нет тестовых данных в CSV")
    
    for row in test_data_csv:
        # Проверка структуры данных
        assert "input" in row
        assert "expected" in row
        
        # Здесь будет логика теста
        # result = some_function(row["input"])
        # assert result == row["expected"]

# =============================================================================
# ШАБЛОН ТЕСТА С ОЖИДАНИЕМ УСЛОВИЯ
# =============================================================================

import time

def test_wait_for_condition():
    """Тест с ожиданием выполнения условия"""
    
    def condition_met():
        # Имитация проверки условия
        return True
    
    def wait_for(condition_func, timeout=5, poll_interval=0.5):
        """Ожидание выполнения условия"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(poll_interval)
        
        return False
    
    # Тест
    result = wait_for(condition_met, timeout=2)
    assert result is True

# =============================================================================
# ШАБЛОН ТЕСТА С ПАРАЛЛЕЛЬНЫМ ВЫПОЛНЕНИЕМ
# =============================================================================

import concurrent.futures

def test_parallel_execution():
    """Тест параллельного выполнения"""
    
    def worker_function(item):
        # Имитация работы
        time.sleep(0.1)
        return item * 2
    
    test_data = [1, 2, 3, 4, 5]
    
    # Параллельное выполнение
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker_function, item) for item in test_data]
        results = [future.result() for future in futures]
    
    expected_results = [2, 4, 6, 8, 10]
    assert results == expected_results

# =============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ТЕСТИРОВАНИЯ
# =============================================================================

class TestDataGenerator:
    """Генератор тестовых данных"""
    
    @staticmethod
    def generate_user_data(count=5):
        """Генерация тестовых пользователей"""
        users = []
        for i in range(count):
            users.append({
                "id": i + 1,
                "name": f"User {i + 1}",
                "email": f"user{i + 1}@example.com",
                "active": i % 2 == 0  # Чередуем активных/неактивных
            })
        return users
    
    @staticmethod
    def generate_test_strings():
        """Генерация различных строк для тестирования"""
        return [
            "",  # Пустая строка
            "a",  # Одиночный символ
            "hello world",  # Нормальная строка
            "Hello World",  # С заглавными буквами
            "12345",  # Только цифры
            "special@#$%chars",  # Специальные символы
            "   spaces   ",  # С пробелами
        ]

# Пример использования генератора
def test_with_generated_data():
    """Тест с использованием сгенерированных данных"""
    generator = TestDataGenerator()
    users = generator.generate_user_data(3)
    
    assert len(users) == 3
    assert all("id" in user for user in users)
    assert all("name" in user for user in users)
    assert all("email" in user for user in users)

"""
🔧 ИСПОЛЬЗОВАНИЕ ШАБЛОНОВ:

1. Копируйте нужный шаблон в свой тестовый файл
2. Адаптируйте под свои нужды
3. Заполняйте секции ARRANGE/ACT/ASSERT
4. Добавляйте свои проверки
5. Запускайте тесты и проверяйте результаты

💡 СОВЕТЫ:
- Всегда начинайте с простого теста
- Постепенно усложняйте логику
- Используйте описательные имена тестов
- Добавляйте комментарии к сложным частям
- Тестируйте одну вещь за раз
"""