"""
🧪 Лабораторная работа 8.1: Collections и структурированные данные для тестирования

🎯 Цель: Освоить расширенные структуры данных Python для эффективного тестирования

📚 Темы:
- Collections module (Counter, defaultdict, deque)
- Named tuples и data classes
- List comprehensions для тестовых данных
- Работа с файлами и сериализацией

⏱️ Время выполнения: 90-120 минут

📝 Инструкции:
1. Выполните все задания по порядку
2. Используйте только структуры данных, изученные в этом модуле
3. Пишите чистый, читаемый код
4. Добавляйте комментарии к сложным частям
"""

from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import dataclass, field
import json
import time
from typing import List, Dict, Optional

# =============================================================================
# ЗАДАНИЕ 1: Анализ результатов тестирования с Counter
# =============================================================================

def analyze_test_results_with_counter():
    """
    🎯 Задание: Используйте Counter для анализа результатов тестирования
    
    Сценарий: У вас есть результаты выполнения 1000 тестов.
    Проанализируйте статистику с помощью Counter.
    """
    
    # Сгенерируем тестовые данные
    import random
    statuses = ["PASSED", "FAILED", "SKIPPED", "ERROR"]
    weights = [0.85, 0.08, 0.05, 0.02]  # Распределение статусов
    
    # TODO: Создайте список из 1000 случайных статусов
    test_results = None  # Ваш код здесь
    
    # TODO: Создайте Counter из результатов
    status_counter = None  # Ваш код здесь
    
    # TODO: Рассчитайте проценты для каждого статуса
    percentages = {}  # Ваш код здесь
    
    # TODO: Найдите самый частый статус
    most_common_status = None  # Ваш код здесь
    
    # TODO: Подсчитайте общее количество проблем (FAILED + ERROR)
    total_problems = None  # Ваш код здесь
    
    # Проверки
    assert len(test_results) == 1000
    assert sum(status_counter.values()) == 1000
    assert most_common_status == "PASSED"
    assert 800 <= status_counter["PASSED"] <= 900
    assert total_problems == status_counter["FAILED"] + status_counter["ERROR"]
    
    print("📊 Статистика результатов тестирования:")
    for status, count in status_counter.most_common():
        percent = percentages[status]
        print(f"  {status}: {count} ({percent:.1f}%)")
    
    print(f"Наиболее частый статус: {most_common_status}")
    print(f"Общее количество проблем: {total_problems}")
    
    return status_counter, percentages

# =============================================================================
# ЗАДАНИЕ 2: Группировка тестов с defaultdict
# =============================================================================

def group_tests_by_module():
    """
    🎯 Задание: Сгруппируйте тесты по модулям с помощью defaultdict
    
    Сценарий: У вас есть список тестов из разных модулей.
    Сгруппируйте их для удобного анализа.
    """
    
    # Тестовые данные
    test_data = [
        {"id": "TC001", "name": "Login Test", "module": "Authentication", "status": "PASSED"},
        {"id": "TC002", "name": "Logout Test", "module": "Authentication", "status": "FAILED"},
        {"id": "TC003", "name": "Payment Test", "module": "Commerce", "status": "PASSED"},
        {"id": "TC004", "name": "Search Test", "module": "UI", "status": "PASSED"},
        {"id": "TC005", "name": "Profile Test", "module": "User", "status": "SKIPPED"},
        {"id": "TC006", "name": "Cart Test", "module": "Commerce", "status": "PASSED"},
        {"id": "TC007", "name": "Register Test", "module": "Authentication", "status": "PASSED"},
        {"id": "TC008", "name": "Wishlist Test", "module": "Commerce", "status": "FAILED"},
    ]
    
    # TODO: Создайте defaultdict для группировки
    grouped_tests = None  # Ваш код здесь
    
    # TODO: Заполните группировку
    # Ваш код здесь
    
    # TODO: Подсчитайте статистику по каждому модулю
    module_stats = {}  # Ваш код здесь
    
    # Проверки
    assert len(grouped_tests["Authentication"]) == 3
    assert len(grouped_tests["Commerce"]) == 3
    assert len(grouped_tests["UI"]) == 1
    assert len(grouped_tests["User"]) == 1
    
    # Проверка статистики
    auth_stats = module_stats["Authentication"]
    assert auth_stats["total"] == 3
    assert auth_stats["passed"] == 2
    assert auth_stats["failed"] == 1
    assert auth_stats["skipped"] == 0
    
    print("📊 Группировка тестов по модулям:")
    for module, tests in grouped_tests.items():
        stats = module_stats[module]
        print(f"  {module}: {stats['total']} тестов")
        print(f"    PASSED: {stats['passed']}, FAILED: {stats['failed']}, SKIPPED: {stats['skipped']}")
    
    return grouped_tests, module_stats

# =============================================================================
# ЗАДАНИЕ 3: Очередь выполнения тестов с deque
# =============================================================================

def test_execution_queue_management():
    """
    🎯 Задание: Управляйте очередью выполнения тестов с помощью deque
    
    Сценарий: Реализуйте систему очереди тестов с приоритетами.
    """
    
    # Тесты с приоритетами (приоритет, название теста)
    test_queue_data = [
        (2, "UI Smoke Tests"),
        (1, "Critical Security Tests"),
        (3, "Edge Case Tests"),
        (1, "Database Connection Tests"),
        (2, "API Integration Tests"),
        (3, "Performance Tests")
    ]
    
    # TODO: Создайте deque из тестовых данных
    test_queue = None  # Ваш код здесь
    
    # TODO: Отсортируйте очередь по приоритету (1 - самый высокий)
    # Ваш код здесь
    
    # TODO: Реализуйте выполнение тестов по очереди
    executed_tests = []  # Ваш код здесь
    execution_log = []   # Ваш код здесь
    
    # Симуляция выполнения
    while test_queue:
        priority, test_name = test_queue.popleft()
        execution_time = round(random.uniform(0.5, 2.0), 2)
        status = "PASSED" if priority <= 2 else random.choice(["PASSED", "FAILED"])
        
        executed_tests.append({
            "name": test_name,
            "priority": priority,
            "status": status,
            "execution_time": execution_time
        })
        
        execution_log.append(f"[Priority {priority}] {test_name} - {status} ({execution_time}s)")
    
    # Проверки
    assert len(executed_tests) == 6
    assert executed_tests[0]["priority"] == 1  # Высший приоритет первым
    assert all(test["execution_time"] >= 0.5 for test in executed_tests)
    
    # Проверка, что тесты с приоритетом 1 выполнились успешно
    critical_tests = [t for t in executed_tests if t["priority"] == 1]
    assert all(t["status"] == "PASSED" for t in critical_tests)
    
    print("📋 Лог выполнения тестов:")
    for log_entry in execution_log:
        print(f"  {log_entry}")
    
    return executed_tests, execution_log

# =============================================================================
# ЗАДАНИЕ 4: Named tuples для структурированных тестовых данных
# =============================================================================

def create_structured_test_data():
    """
    🎯 Задание: Создайте структурированные тестовые данные с named tuples
    
    Сценарий: Организуйте тестовые данные в читаемую структуру.
    """
    
    # TODO: Создайте named tuples для тестовых данных
    TestCase = None  # Ваш код здесь
    TestResult = None  # Ваш код здесь
    
    # TODO: Создайте тестовые случаи
    test_cases = [
        # Создайте 3-5 тестовых случаев
        # Ваш код здесь
    ]
    
    # TODO: Симулируйте выполнение тестов
    test_results = []  # Ваш код здесь
    
    # Симуляция выполнения
    import random
    for case in test_cases:
        execution_time = round(random.uniform(0.5, 3.0), 2)
        status = random.choice(["PASSED", "FAILED"]) if "negative" in case.name.lower() else "PASSED"
        
        result = TestResult(
            test_case=case,
            status=status,
            execution_time=execution_time,
            error_message="Invalid input" if status == "FAILED" else None
        )
        test_results.append(result)
    
    # TODO: Проанализируйте результаты
    passed_count = None  # Ваш код здесь
    failed_count = None  # Ваш код здесь
    avg_execution_time = None  # Ваш код здесь
    
    # Проверки
    assert len(test_cases) >= 3
    assert len(test_results) == len(test_cases)
    assert passed_count + failed_count == len(test_results)
    assert avg_execution_time > 0
    
    print("📊 Результаты структурированного тестирования:")
    print(f"Всего тестов: {len(test_cases)}")
    print(f"Успешно: {passed_count}")
    print(f"Провалено: {failed_count}")
    print(f"Среднее время выполнения: {avg_execution_time:.2f} сек")
    
    # Показать детали проваленных тестов
    failed_tests = [r for r in test_results if r.status == "FAILED"]
    if failed_tests:
        print("\n❌ Проваленные тесты:")
        for result in failed_tests:
            print(f"  - {result.test_case.name}: {result.error_message}")
    
    return test_cases, test_results

# =============================================================================
# ЗАДАНИЕ 5: Data classes для сложных структур
# =============================================================================

@dataclass
class TestEnvironment:
    """Конфигурация тестового окружения"""
    name: str
    base_url: str
    browser: str
    timeout: int = 30
    headless: bool = True

@dataclass
class TestSuiteConfig:
    """Конфигурация набора тестов"""
    name: str
    module: str
    environment: TestEnvironment
    parallel_executors: int = 1
    retry_attempts: int = 3

def create_test_configuration():
    """
    🎯 Задание: Создайте сложную конфигурацию тестов с data classes
    
    Сценарий: Настройте тестовое окружение для разных сценариев.
    """
    
    # TODO: Создайте конфигурации для разных окружений
    environments = {
        "development": None,  # Ваш код здесь
        "staging": None,      # Ваш код здесь
        "production": None    # Ваш код здесь
    }
    
    # TODO: Создайте конфигурации наборов тестов
    test_suites = [
        # Создайте 2-3 набора тестов
        # Ваш код здесь
    ]
    
    # TODO: Сериализуйте конфигурации в JSON
    config_data = {
        "environments": {},
        "test_suites": []
    }
    
    # Преобразование в словари для сериализации
    for env_name, env in environments.items():
        config_data["environments"][env_name] = {
            "name": env.name,
            "base_url": env.base_url,
            "browser": env.browser,
            "timeout": env.timeout,
            "headless": env.headless
        }
    
    for suite in test_suites:
        config_data["test_suites"].append({
            "name": suite.name,
            "module": suite.module,
            "environment": suite.environment.name,
            "parallel_executors": suite.parallel_executors,
            "retry_attempts": suite.retry_attempts
        })
    
    # TODO: Сохраните конфигурацию в файл
    # Ваш код здесь (сохранение в test_config.json)
    
    # TODO: Загрузите и проверьте конфигурацию
    # Ваш код здесь (загрузка из файла)
    
    # Проверки
    assert len(environments) == 3
    assert len(test_suites) >= 2
    assert environments["development"].timeout == 30
    assert environments["production"].headless == True
    
    print("🔧 Созданные конфигурации:")
    for env_name, env in environments.items():
        print(f"  {env_name}: {env.base_url} (timeout: {env.timeout}s)")
    
    print(f"\n📋 Наборы тестов: {len(test_suites)}")
    for suite in test_suites:
        print(f"  {suite.name} -> {suite.environment.name}")
    
    return environments, test_suites, config_data

# =============================================================================
# ЗАДАНИЕ 6: List comprehensions для генерации тестовых данных
# =============================================================================

def generate_test_data_with_comprehensions():
    """
    🎯 Задание: Сгенерируйте тестовые данные с помощью comprehensions
    
    Сценарий: Создайте большие объемы тестовых данных эффективно.
    """
    
    # TODO: Сгенерируйте список пользователей для тестирования
    # Формат: user_001, user_002, ... user_100
    test_users = None  # Ваш код здесь
    
    # TODO: Создайте тестовые email адреса
    # Формат: user001@test.com, user002@test.com, ...
    test_emails = None  # Ваш код здесь
    
    # TODO: Сгенерируйте тестовые пароли с разной сложностью
    passwords = None  # Ваш код здесь
    
    # TODO: Создайте комбинированные тестовые данные
    user_test_data = None  # Ваш код здесь
    
    # TODO: Отфильтруйте активных пользователей (четные ID)
    active_users = None  # Ваш код здесь
    
    # TODO: Создайте отчет по категориям сложности паролей
    password_categories = {
        "simple": None,    # Ваш код здесь
        "medium": None,    # Ваш код здесь
        "complex": None    # Ваш код здесь
    }
    
    # Проверки
    assert len(test_users) == 100
    assert len(test_emails) == 100
    assert len(passwords) == 100
    assert len(active_users) == 50  # Половина пользователей активны
    assert sum(len(cat) for cat in password_categories.values()) == 100
    
    # Проверка форматов
    assert test_users[0] == "user_001"
    assert test_emails[0] == "user001@test.com"
    assert all("@" in email for email in test_emails)
    
    print("📊 Сгенерированные тестовые данные:")
    print(f"Пользователей: {len(test_users)}")
    print(f"Активных пользователей: {len(active_users)}")
    print(f"Категории паролей:")
    for category, count in password_categories.items():
        print(f"  {category}: {len(count)}")
    
    # Показать примеры
    print(f"\n📝 Примеры данных:")
    print(f"Первый пользователь: {user_test_data[0]}")
    print(f"Последний пользователь: {user_test_data[-1]}")
    
    return test_users, test_emails, passwords, user_test_data, active_users, password_categories

# =============================================================================
# ЗАДАНИЕ 7: Интеграционное задание - Система управления тестовыми данными
# =============================================================================

def integrated_test_data_management():
    """
    🎯 Задание: Создайте комплексную систему управления тестовыми данными
    
    Сценарий: Объедините все изученные структуры данных в единую систему.
    """
    
    # Используем все ранее созданные функции
    print("🚀 Запуск интеграционной системы управления тестовыми данными")
    print("=" * 70)
    
    try:
        # 1. Анализ результатов
        print("\n1️⃣ Анализ результатов тестирования...")
        counter_results, percentages = analyze_test_results_with_counter()
        
        # 2. Группировка тестов
        print("\n2️⃣ Группировка тестов по модулям...")
        grouped_tests, module_stats = group_tests_by_module()
        
        # 3. Управление очередью
        print("\n3️⃣ Управление очередью выполнения...")
        executed_tests, execution_log = test_execution_queue_management()
        
        # 4. Структурированные данные
        print("\n4️⃣ Создание структурированных тестовых данных...")
        test_cases, test_results = create_structured_test_data()
        
        # 5. Конфигурации
        print("\n5️⃣ Настройка тестовых конфигураций...")
        environments, test_suites, config_data = create_test_configuration()
        
        # 6. Генерация данных
        print("\n6️⃣ Генерация тестовых данных...")
        test_users, test_emails, passwords, user_data, active_users, pwd_cats = generate_test_data_with_comprehensions()
        
        # Финальный отчет
        print("\n" + "=" * 70)
        print("🏆 Система управления тестовыми данными успешно запущена!")
        print("\n📊 Итоговая статистика:")
        print(f"  • Проанализировано результатов: {sum(counter_results.values())}")
        print(f"  • Сгруппировано тестов: {sum(len(tests) for tests in grouped_tests.values())}")
        print(f"  • Выполнено тестов: {len(executed_tests)}")
        print(f"  • Создано структурированных тестов: {len(test_cases)}")
        print(f"  • Настроено окружений: {len(environments)}")
        print(f"  • Сгенерировано пользовательских данных: {len(test_users)}")
        
        # Сохраняем общий отчет
        final_report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "statistics": {
                "total_results_analyzed": sum(counter_results.values()),
                "modules_tested": len(grouped_tests),
                "tests_executed": len(executed_tests),
                "structured_test_cases": len(test_cases),
                "environments_configured": len(environments),
                "user_data_generated": len(test_users)
            },
            "configuration_summary": {
                "environments": list(environments.keys()),
                "test_suites": [suite.name for suite in test_suites]
            }
        }
        
        with open('final_integration_report.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Отчет сохранен в final_integration_report.json")
        print("🎉 Все компоненты системы работают корректно!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка в интеграционной системе: {e}")
        print("💡 Проверьте реализацию всех предыдущих заданий")
        return False

# =============================================================================
# Функция запуска всех заданий
# =============================================================================

def run_all_labs():
    """Запускает все лабораторные задания"""
    print("🔬 Запуск лабораторной работы 8.1: Collections и структурированные данные")
    print("=" * 80)
    
    try:
        # Выполняем все задания по порядку
        print("Выполняем задания...")
        
        # Для экономии времени в демонстрации, запускаем только интеграционное задание
        # В реальной практике студенты выполняют все задания по отдельности
        success = integrated_test_data_management()
        
        if success:
            print("\n" + "=" * 80)
            print("🎉 Лабораторная работа 8.1 завершена успешно!")
            print("🏆 Вы освоили расширенные структуры данных для тестирования!")
        else:
            print("\n❌ Возникли ошибки в выполнении заданий")
            
    except Exception as e:
        print(f"\n💥 Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()

# Запуск при импорте как модуля
if __name__ == "__main__":
    run_all_labs()