#!/usr/bin/env python3
"""
Скрипт для автоматической генерации моделей SQLAlchemy из базы данных
с использованием настроек из .env файла
"""

import os
import subprocess
from dotenv import load_dotenv

def load_env_config():
    """Загрузка конфигурации из .env файла"""
    # Загружаем переменные окружения из .env
    load_dotenv()
    
    # Получаем параметры подключения
    config = {
        'host': os.getenv('HOST', 'localhost'),
        'port': os.getenv('PORT', '5432'),
        'user': os.getenv('USER', 'postgres'),
        'password': os.getenv('PASSWORD', ''),
        'database': os.getenv('DATABASE', 'demo')
    }
    
    return config

def generate_models(config, output_file='models.py', schema='bookings'):
    """
    Генерация моделей SQLAlchemy с помощью sqlacodegen_v2
    
    Args:
        config (dict): Конфигурация подключения к БД
        output_file (str): Имя выходного файла
        schema (str): Схема базы данных
    """
    # Формируем строку подключения
    connection_string = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    
    # Команда для выполнения с декларативным стилем
    cmd = [
        'sqlacodegen_v2',
        connection_string,
        '--schema', 'bookings',  # Схема bookings
        '--outfile', output_file,
        '--generator', 'declarative',  # Декларативный стиль
    ]
    
    print(f"Генерация моделей из базы данных: {config['database']}")
    print(f"Строка подключения: {connection_string}")
    print(f"Выходной файл: {output_file}")
    
    try:
        # Выполняем команду
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Модели успешно сгенерированы!")
        print(f"Файл сохранен как: {output_file}")
        
        if result.stdout:
            print("Вывод:")
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
        print("❌ Ошибка при генерации моделей:")
        print(f"Код ошибки: {e.returncode}")
        print(f"Ошибка: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Команда sqlacodegen_v2 не найдена. Убедитесь, что она установлена:")
        print("pip install sqlacodegen-v2")
        return False
    
    return True

def main():
    """Основная функция"""
    print("🔧 Генератор моделей SQLAlchemy из .env конфигурации")
    print("=" * 50)
    
    # Загружаем конфигурацию
    config = load_env_config()
    
    # Показываем текущую конфигурацию (без пароля)
    print("Текущая конфигурация:")
    print(f"  Хост: {config['host']}")
    print(f"  Порт: {config['port']}")
    print(f"  Пользователь: {config['user']}")
    print(f"  База данных: {config['database']}")
    print(f"  Пароль: {'*' * len(config['password']) if config['password'] else 'не задан'}")
    print()
    
    # Спрашиваем подтверждение
    response = input("Продолжить генерацию моделей? (y/N): ").strip().lower()
    
    if response in ['y', 'yes', 'да']:
        # Генерируем модели
        success = generate_models(config)
        
        if success:
            print("\n🎉 Генерация завершена успешно!")
            print("Вы можете найти сгенерированные модели в файле models.py")
        else:
            print("\n💥 Генерация завершена с ошибками")
    else:
        print("Отменено пользователем")

if __name__ == "__main__":
    main()