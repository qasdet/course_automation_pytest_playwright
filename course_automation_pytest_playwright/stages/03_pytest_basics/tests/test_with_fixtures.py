"""
test_with_fixtures.py - Примеры тестов с использованием фикстур

Этот файл демонстрирует различные способы использования фикстур
в pytest для разных сценариев тестирования.
"""

import pytest
import json
import os
import sqlite3
from unittest.mock import Mock, patch


# ==================== ТЕСТЫ С БАЗОВЫМИ ФИКСТУРАМИ ====================

def test_temp_file_fixture(temp_file):
    """
    Тест использования фикстуры временного файла
    
    Args:
        temp_file: Фикстура временного файла
    """
    # Проверяем, что файл существует
    assert os.path.exists(temp_file)
    
    # Читаем содержимое файла
    with open(temp_file, 'r') as f:
        content = f.read()
    
    # Проверяем содержимое
    assert content == "test content"


def test_json_file_fixture(sample_json_file):
    """
    Тест использования фикстуры JSON файла
    
    Args:
        sample_json_file: Фикстура JSON файла
    """
    # Проверяем, что файл существует
    assert os.path.exists(sample_json_file)
    
    # Читаем и парсим JSON
    with open(sample_json_file, 'r') as f:
        data = json.load(f)
    
    # Проверяем структуру данных
    assert "users" in data
    assert "settings" in data
    assert len(data["users"]) == 2
    assert data["settings"]["timeout"] == 30


# ==================== ТЕСТЫ С БАЗОЙ ДАННЫХ ====================

def test_database_connection(sqlite_db):
    """
    Тест подключения к базе данных
    
    Args:
        sqlite_db: Фикстура базы данных
    """
    # Проверяем, что можем выполнять запросы
    cursor = sqlite_db.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    assert count == 2


def test_database_operations(db_cursor):
    """
    Тест операций с базой данных через курсор
    
    Args:
        db_cursor: Фикстура курсора базы данных
    """
    # Тест SELECT
    db_cursor.execute("SELECT name FROM users WHERE id = ?", (1,))
    result = db_cursor.fetchone()
    assert result[0] == "Alice"
    
    # Тест INSERT
    db_cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Charlie", "charlie@example.com")
    )
    
    # Тест UPDATE
    db_cursor.execute(
        "UPDATE users SET name = ? WHERE id = ?",
        ("Alice Updated", 1)
    )
    
    # Тест DELETE
    db_cursor.execute("DELETE FROM users WHERE id = ?", (2,))


# ==================== ТЕСТЫ С МОКАМИ ====================

def test_mock_http_client(mock_http_client):
    """
    Тест использования мока HTTP клиента
    
    Args:
        mock_http_client: Фикстура мока HTTP клиента
    """
    # Тест GET запроса
    response = mock_http_client.get("https://api.example.com/users")
    
    assert response.status_code == 200
    assert response.json() == {"message": "success"}
    mock_http_client.get.assert_called_once_with("https://api.example.com/users")
    
    # Тест POST запроса
    data = {"name": "New User"}
    response = mock_http_client.post("https://api.example.com/users", json=data)
    
    assert response.status_code == 201
    assert response.json()["created"] == True
    mock_http_client.post.assert_called_with(
        "https://api.example.com/users", 
        json=data
    )


def test_mock_api_response(mock_api_response):
    """
    Тест использования фикстуры с данными API
    
    Args:
        mock_api_response: Фикстура данных API
    """
    # Проверяем структуру ответа
    assert mock_api_response["status"] == "success"
    assert "data" in mock_api_response
    assert "user" in mock_api_response["data"]
    
    user = mock_api_response["data"]["user"]
    assert user["id"] == 1
    assert user["name"] == "Test User"


# ==================== ТЕСТЫ С ТЕСТОВЫМИ ДАННЫМИ ====================

def test_user_data_fixture(user_data):
    """
    Тест использования фикстуры данных пользователя
    
    Args:
        user_data: Фикстура данных пользователя
    """
    # Проверяем обязательные поля
    required_fields = ["id", "name", "email", "age", "active"]
    for field in required_fields:
        assert field in user_data
    
    # Проверяем типы данных
    assert isinstance(user_data["id"], int)
    assert isinstance(user_data["name"], str)
    assert isinstance(user_data["age"], int)
    assert isinstance(user_data["active"], bool)
    
    # Проверяем значения
    assert user_data["id"] == 1
    assert user_data["active"] == True


def test_product_data_fixture(product_data):
    """
    Тест использования фикстуры данных продукта
    
    Args:
        product_data: Фикстура данных продукта
    """
    # Проверяем структуру продукта
    assert product_data["name"] == "Premium Widget"
    assert product_data["price"] == 99.99
    assert product_data["in_stock"] == True
    assert product_data["rating"] == 4.5


# ==================== ТЕСТЫ С УТИЛИТАМИ ====================

def test_caplog_fixture(caplog_handler):
    """
    Тест захвата логов
    
    Args:
        caplog_handler: Фикстура захвата логов
    """
    import logging
    
    logger = logging.getLogger("test_logger")
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")
    
    # Проверяем захваченные сообщения
    messages = caplog_handler.get_messages()
    assert "Test info message" in messages
    assert "Test warning message" in messages
    assert "Test error message" in messages
    
    # Проверяем уровни логов
    records = caplog_handler.get_records()
    levels = [record.levelname for record in records]
    assert "INFO" in levels
    assert "WARNING" in levels
    assert "ERROR" in levels


def test_environment_vars_fixture(environment_vars):
    """
    Тест переменных окружения
    
    Args:
        environment_vars: Фикстура переменных окружения
    """
    # Проверяем, что переменные установлены
    assert os.environ["TEST_MODE"] == "true"
    assert os.environ["API_KEY"] == "test-key-123"
    assert os.environ["DEBUG"] == "true"
    
    # Проверяем все переменные из фикстуры
    for key, value in environment_vars.items():
        assert os.environ[key] == value


# ==================== ТЕСТЫ С ПАРАМЕТРИЗАЦИЕЙ ====================

@pytest.mark.parametrize("test_input,expected", [
    (1, "odd"),
    (2, "even"),
    (3, "odd"),
    (4, "even"),
])
def test_number_classification(test_input, expected):
    """
    Параметризованный тест классификации чисел
    
    Args:
        test_input: Входное число
        expected: Ожидаемый результат
    """
    result = "even" if test_input % 2 == 0 else "odd"
    assert result == expected


def test_expensive_resource(expensive_resource):
    """
    Тест использования дорогостоящей фикстуры
    
    Args:
        expensive_resource: Фикстура дорогостоящего ресурса
    """
    # Проверяем, что ресурс доступен
    assert expensive_resource == "expensive-resource-123"
    
    # Имитация использования ресурса
    result = f"processed-{expensive_resource}"
    assert result == "processed-expensive-resource-123"


# ==================== ТЕСТЫ СО СЛОЖНЫМИ СЦЕНАРИЯМИ ====================

def test_integration_scenario(temp_file, mock_http_client, user_data):
    """
    Интеграционный тест с несколькими фикстурами
    
    Args:
        temp_file: Фикстура временного файла
        mock_http_client: Фикстура HTTP клиента
        user_data: Фикстура данных пользователя
    """
    # Шаг 1: Сохраняем данные пользователя во временный файл
    user_json = json.dumps(user_data)
    with open(temp_file, 'w') as f:
        f.write(user_json)
    
    # Шаг 2: Читаем данные из файла
    with open(temp_file, 'r') as f:
        saved_data = json.load(f)
    
    # Шаг 3: Отправляем данные через мок API
    response = mock_http_client.post("https://api.example.com/users", json=saved_data)
    
    # Проверки
    assert saved_data["id"] == user_data["id"]
    assert response.status_code == 201
    assert response.json()["created"] == True


@pytest.mark.database
def test_database_with_multiple_operations(sqlite_db, user_data):
    """
    Тест комплексных операций с базой данных
    
    Args:
        sqlite_db: Фикстура базы данных
        user_data: Фикстура данных пользователя
    """
    cursor = sqlite_db.cursor()
    
    # Добавляем нового пользователя
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (user_data["name"], user_data["email"])
    )
    
    # Получаем ID нового пользователя
    cursor.execute("SELECT last_insert_rowid()")
    new_user_id = cursor.fetchone()[0]
    
    # Проверяем, что пользователь добавлен
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    assert total_users == 3  # 2 существующих + 1 новый
    
    # Проверяем данные нового пользователя
    cursor.execute("SELECT name, email FROM users WHERE id = ?", (new_user_id,))
    result = cursor.fetchone()
    assert result[0] == user_data["name"]
    assert result[1] == user_data["email"]


# ==================== ТЕСТЫ С ПОЛЬЗОВАТЕЛЬСКИМИ ФИКСТУРАМИ ====================

def test_utility_functions(test_utils):
    """
    Тест пользовательских утилитных функций
    
    Args:
        test_utils: Фикстура утилитных функций
    """
    # Тест приблизительного равенства
    test_utils.assert_approx_equal(1.0000001, 1.0, tolerance=1e-5)
    
    # Тест подмножества словаря
    full_dict = {"a": 1, "b": 2, "c": 3}
    subset = {"a": 1, "b": 2}
    test_utils.assert_dict_subset(subset, full_dict)
    
    # Тест создания временного файла
    temp_path = test_utils.create_temp_file_with_content("hello world", ".txt")
    assert os.path.exists(temp_path)
    
    with open(temp_path, 'r') as f:
        content = f.read()
    assert content == "hello world"
    
    # Очистка
    os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])