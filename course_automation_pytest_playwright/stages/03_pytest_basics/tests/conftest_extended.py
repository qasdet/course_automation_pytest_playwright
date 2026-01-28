"""
conftest.py - Глобальные фикстуры и конфигурация pytest

Этот файл содержит общие фикстуры, хуки и конфигурацию,
которые могут использоваться во всех тестах проекта.
"""

import pytest
import tempfile
import json
import os
import sqlite3
from unittest.mock import Mock, patch
from typing import Generator, Dict, Any
import logging


# ==================== БАЗОВЫЕ ФИКСТУРЫ ====================

@pytest.fixture
def temp_directory() -> Generator[str, None, None]:
    """
    Фикстура для временной директории
    
    Yields:
        str: Путь к временной директории
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """
    Фикстура для временного файла
    
    Yields:
        str: Путь к временному файлу
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    try:
        os.unlink(temp_path)
    except OSError:
        pass


@pytest.fixture
def sample_json_file() -> Generator[str, None, None]:
    """
    Фикстура для временного JSON файла с тестовыми данными
    
    Yields:
        str: Путь к JSON файлу
    """
    test_data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "settings": {
            "timeout": 30,
            "retries": 3,
            "debug": True
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f, indent=2)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    try:
        os.unlink(temp_path)
    except OSError:
        pass


# ==================== ФИКСТУРЫ ДЛЯ БАЗ ДАННЫХ ====================

@pytest.fixture
def sqlite_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Фикстура для временной SQLite базы данных
    
    Yields:
        sqlite3.Connection: Соединение с базой данных
    """
    # Создаем временную базу данных в памяти
    conn = sqlite3.connect(':memory:')
    
    # Создаем таблицы
    conn.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    conn.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # Добавляем тестовые данные
    conn.executemany(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        [('Alice', 'alice@example.com'), ('Bob', 'bob@example.com')]
    )
    
    conn.executemany(
        'INSERT INTO products (name, price) VALUES (?, ?)',
        [('Laptop', 999.99), ('Mouse', 29.99), ('Keyboard', 79.99)]
    )
    
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def db_cursor(sqlite_db) -> sqlite3.Cursor:
    """
    Фикстура для курсора базы данных
    
    Args:
        sqlite_db: Фикстура базы данных
        
    Yields:
        sqlite3.Cursor: Курсор базы данных
    """
    cursor = sqlite_db.cursor()
    yield cursor


# ==================== МОКИ И СИМУЛЯЦИИ ====================

@pytest.fixture
def mock_http_client() -> Mock:
    """
    Фикстура для мока HTTP клиента
    
    Returns:
        Mock: Мок объект HTTP клиента
    """
    client = Mock()
    
    # Настройка возвращаемых значений
    client.get.return_value = Mock(
        status_code=200,
        json=lambda: {"message": "success"}
    )
    
    client.post.return_value = Mock(
        status_code=201,
        json=lambda: {"id": 123, "created": True}
    )
    
    return client


@pytest.fixture
def mock_api_response() -> Dict[str, Any]:
    """
    Фикстура для стандартного ответа API
    
    Returns:
        Dict[str, Any]: Словарь с тестовыми данными API
    """
    return {
        "status": "success",
        "data": {
            "user": {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com"
            },
            "timestamp": "2023-01-01T00:00:00Z"
        }
    }


# ==================== ТЕСТОВЫЕ ДАННЫЕ ====================

@pytest.fixture
def user_data() -> Dict[str, Any]:
    """
    Фикстура с тестовыми данными пользователя
    
    Returns:
        Dict[str, Any]: Данные тестового пользователя
    """
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "active": True
    }


@pytest.fixture
def product_data() -> Dict[str, Any]:
    """
    Фикстура с тестовыми данными продукта
    
    Returns:
        Dict[str, Any]: Данные тестового продукта
    """
    return {
        "id": 1,
        "name": "Premium Widget",
        "price": 99.99,
        "category": "electronics",
        "in_stock": True,
        "rating": 4.5
    }


# ==================== УТИЛИТНЫЕ ФИКСТУРЫ ====================

@pytest.fixture
def caplog_handler() -> Generator[logging.Handler, None, None]:
    """
    Фикстура для захвата логов
    
    Yields:
        logging.Handler: Обработчик логов для тестирования
    """
    import logging
    
    class LogCaptureHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.records = []
        
        def emit(self, record):
            self.records.append(record)
        
        def get_messages(self):
            return [record.getMessage() for record in self.records]
        
        def get_records(self):
            return self.records[:]
    
    handler = LogCaptureHandler()
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    yield handler
    
    logger.removeHandler(handler)


@pytest.fixture
def environment_vars() -> Generator[Dict[str, str], None, None]:
    """
    Фикстура для временных переменных окружения
    
    Yields:
        Dict[str, str]: Словарь переменных окружения
    """
    original_env = dict(os.environ)
    
    test_env = {
        'TEST_MODE': 'true',
        'API_KEY': 'test-key-123',
        'DATABASE_URL': 'sqlite:///:memory:',
        'DEBUG': 'true'
    }
    
    os.environ.update(test_env)
    yield test_env
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# ==================== СЛОЖНЫЕ ФИКСТУРЫ ====================

@pytest.fixture(scope="session")
def expensive_resource():
    """
    Фикстура с session scope для дорогостоящих ресурсов
    
    Returns:
        str: Идентификатор ресурса
    """
    # Имитация создания дорогого ресурса
    resource_id = "expensive-resource-123"
    print(f"\n🔧 Создание дорогостоящего ресурса: {resource_id}")
    yield resource_id
    print(f"\n🧹 Очистка дорогостоящего ресурса: {resource_id}")


@pytest.fixture
def mock_external_service():
    """
    Фикстура для мока внешнего сервиса с контекстным менеджером
    
    Returns:
        Mock: Мок внешнего сервиса
    """
    service = Mock()
    
    # Имитация различных методов сервиса
    service.process_data.return_value = {"processed": True, "count": 42}
    service.validate_input.return_value = True
    service.get_status.return_value = "healthy"
    
    # Имитация исключений
    service.fail_method.side_effect = Exception("Service temporarily unavailable")
    
    return service


# ==================== ПАРАМЕТРИЗОВАННЫЕ ФИКСТУРЫ ====================

@pytest.fixture(params=[1, 2, 3, 4, 5])
def number_sequence(request) -> int:
    """
    Параметризованная фикстура для последовательности чисел
    
    Args:
        request: Объект запроса pytest
        
    Returns:
        int: Число из последовательности
    """
    return request.param


@pytest.fixture(params=['small', 'medium', 'large'])
def data_size(request) -> str:
    """
    Параметризованная фикстура для размеров данных
    
    Args:
        request: Объект запроса pytest
        
    Returns:
        str: Размер данных
    """
    return request.param


# ==================== ХУКИ PYTEST ====================

def pytest_configure(config):
    """
    Хук конфигурации pytest
    
    Args:
        config: Объект конфигурации pytest
    """
    # Добавляем пользовательские маркеры
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "database: marks tests that use database"
    )
    config.addinivalue_line(
        "markers", "api: marks tests that use external APIs"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания отчетов о тестах
    
    Args:
        item: Тестовый элемент
        call: Вызов теста
    """
    # Добавляем информацию о медленных тестах
    if call.when == "call" and call.excinfo is None:
        duration = call.stop - call.start
        if duration > 1.0:  # Более 1 секунды
            item.user_properties.append(("duration", duration))


# ==================== УТИЛИТНЫЕ ФУНКЦИИ ====================

@pytest.fixture
def test_utils():
    """
    Фикстура с утилитными функциями для тестов
    
    Returns:
        object: Объект с утилитными методами
    """
    class TestUtils:
        @staticmethod
        def assert_approx_equal(actual, expected, tolerance=1e-6):
            """Проверка приблизительного равенства чисел"""
            assert abs(actual - expected) < tolerance
        
        @staticmethod
        def assert_dict_subset(subset, superset):
            """Проверка, что subset является подмножеством superset"""
            for key, value in subset.items():
                assert key in superset
                assert superset[key] == value
        
        @staticmethod
        def create_temp_file_with_content(content, suffix=''):
            """Создание временного файла с содержимым"""
            with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
                f.write(content)
                return f.name
        
        @staticmethod
        def mock_time(return_value):
            """Декоратор для мока времени"""
            def decorator(func):
                with patch('time.time', return_value=return_value):
                    return func()
            return decorator
    
    return TestUtils()