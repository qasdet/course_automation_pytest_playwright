# Модуль 8: Структуры данных для тестировщиков

## 🎯 Цели модуля (2 недели / 8 занятий)

**По окончании модуля студент сможет:**
- Эффективно использовать расширенные структуры данных Python для тестирования
- Работать с большими объемами тестовых данных
- Создавать генераторы и фабрики тестовых данных
- Обрабатывать конфигурационные файлы различных форматов
- Структурировать результаты тестирования
- Оптимизировать производительность тестов через правильный выбор структур данных

## 👨‍🏫 Методические материалы для преподавателя

### Общие рекомендации по преподаванию:

**🎯 Основной подход:**
- Связывать каждую структуру данных с реальными тестовыми сценариями
- Демонстрировать performance benefits на практике
- Показывать как выбор правильной структуры влияет на читаемость тестов
- Объяснять trade-offs между разными подходами

**📋 Необходимые материалы:**
- Примеры реальных тестовых данных (JSON, CSV файлы)
- Performance benchmarks разных структур данных
- Шаблоны для генерации тестовых данных
- Примеры плохого и хорошего кода

**⏰ Структура занятий:**
- 15 мин: Разбор домашнего задания
- 20 мин: Новая теория с примерами
- 30 мин: Практические упражнения
- 15 мин: Перерыв
- 25 мин: Работа с реальными тестовыми данными
- 15 мин: Подведение итогов и домашнее задание

## 📚 Теоретические основы

### Введение в расширенные структуры данных

#### Почему важно для тестировщиков?

```python
# ❌ Плохой подход - базовые структуры
def bad_test_data_management():
    # Не структурированные данные
    test_users = [
        ["user1", "pass1", "active"],
        ["user2", "pass2", "inactive"],
        ["user3", "pass3", "active"]
    ]
    
    # Сложная обработка
    active_users = []
    for user in test_users:
        if user[2] == "active":
            active_users.append({"username": user[0], "password": user[1]})
    
    return active_users

# ✅ Хороший подход - структурированные данные
from collections import namedtuple

UserTestData = namedtuple('UserTestData', ['username', 'password', 'status'])

def good_test_data_management():
    # Структурированные данные
    test_users = [
        UserTestData("user1", "pass1", "active"),
        UserTestData("user2", "pass2", "inactive"),
        UserTestData("user3", "pass3", "active")
    ]
    
    # Простая обработка
    active_users = [user for user in test_users if user.status == "active"]
    
    return active_users

# Performance comparison
import time

def benchmark_approaches():
    # Генерируем большие объемы данных
    large_dataset = [("user"+str(i), "pass"+str(i), "active" if i%2 else "inactive") 
                     for i in range(10000)]
    
    # Тестируем плохой подход
    start = time.time()
    result1 = bad_test_data_management.__code__.replace(co_consts=(large_dataset,))
    time1 = time.time() - start
    
    # Тестируем хороший подход
    start = time.time()
    structured_data = [UserTestData(*user) for user in large_dataset]
    result2 = [user for user in structured_data if user.status == "active"]
    time2 = time.time() - start
    
    print(f"Базовый подход: {time1:.4f} сек")
    print(f"Структурированный: {time2:.4f} сек")
    print(f"Улучшение: {(time1/time2):.1f}x быстрее")
```

## 🛠️ Collections Module для тестирования

### Counter - анализ результатов тестирования

```python
from collections import Counter

def analyze_test_results(test_results):
    """Анализ результатов тестирования с помощью Counter"""
    
    # Пример результатов тестов
    test_results = [
        "PASSED", "FAILED", "PASSED", "SKIPPED", "PASSED",
        "FAILED", "PASSED", "PASSED", "ERROR", "PASSED"
    ]
    
    # Подсчет статусов
    status_counter = Counter(test_results)
    
    print("📊 Статистика по статусам:")
    for status, count in status_counter.items():
        percentage = (count / len(test_results)) * 100
        print(f"  {status}: {count} ({percentage:.1f}%)")
    
    # Находим наиболее частый статус
    most_common = status_counter.most_common(1)[0]
    print(f"Наиболее частый статус: {most_common[0]} ({most_common[1]} раз)")
    
    # Проверяем критические ошибки
    critical_statuses = status_counter["FAILED"] + status_counter["ERROR"]
    if critical_statuses > 0:
        print(f"⚠️  Обнаружено {critical_statuses} критических проблем")
    
    return status_counter

# Пример использования в тестах
def test_counter_analysis():
    """Тест анализа результатов с Counter"""
    
    # Имитация результатов тестирования
    results = ["PASSED"] * 85 + ["FAILED"] * 10 + ["SKIPPED"] * 5
    
    counter = analyze_test_results(results)
    
    # Проверки
    assert counter["PASSED"] == 85
    assert counter["FAILED"] == 10
    assert counter["SKIPPED"] == 5
    assert len(results) == 100
    
    print("✅ Counter analysis работает корректно")

# Advanced Counter usage
def advanced_test_analysis():
    """Продвинутый анализ с несколькими метриками"""
    
    # Сложная структура результатов
    detailed_results = [
        {"module": "auth", "status": "PASSED", "execution_time": 1.2},
        {"module": "payment", "status": "FAILED", "execution_time": 2.5},
        {"module": "auth", "status": "PASSED", "execution_time": 1.1},
        {"module": "profile", "status": "PASSED", "execution_time": 0.8},
        {"module": "payment", "status": "PASSED", "execution_time": 2.1},
    ]
    
    # Анализ по модулям
    module_counter = Counter(result["module"] for result in detailed_results)
    status_by_module = {}
    
    for result in detailed_results:
        module = result["module"]
        if module not in status_by_module:
            status_by_module[module] = Counter()
        status_by_module[module][result["status"]] += 1
    
    print("📊 Анализ по модулям:")
    for module, statuses in status_by_module.items():
        total = sum(statuses.values())
        passed_rate = (statuses["PASSED"] / total) * 100
        print(f"  {module}: {total} тестов, {passed_rate:.1f}% прошло")
    
    return module_counter, status_by_module
```

### DefaultDict - упрощение группировки данных

```python
from collections import defaultdict

def group_test_results_by_module(test_results):
    """Группировка результатов тестов по модулям"""
    
    # Группировка с обычным словарем
    grouped_bad = {}
    for result in test_results:
        module = result["module"]
        if module not in grouped_bad:
            grouped_bad[module] = []
        grouped_bad[module].append(result)
    
    # Группировка с defaultdict (лучше)
    grouped_good = defaultdict(list)
    for result in test_results:
        grouped_good[result["module"]].append(result)
    
    return dict(grouped_good)

# Пример использования
def test_defaultdict_grouping():
    """Тест группировки с defaultdict"""
    
    test_data = [
        {"module": "auth", "test": "login", "status": "PASSED"},
        {"module": "auth", "test": "logout", "status": "FAILED"},
        {"module": "payment", "test": "transaction", "status": "PASSED"},
        {"module": "auth", "test": "password_reset", "status": "PASSED"},
        {"module": "profile", "test": "update", "status": "PASSED"},
    ]
    
    grouped = group_test_results_by_module(test_data)
    
    # Проверки
    assert len(grouped["auth"]) == 3
    assert len(grouped["payment"]) == 1
    assert len(grouped["profile"]) == 1
    
    # Проверка содержимого
    auth_tests = [test["test"] for test in grouped["auth"]]
    assert "login" in auth_tests
    assert "logout" in auth_tests
    assert "password_reset" in auth_tests
    
    print("✅ DefaultDict grouping работает корректно")
    return grouped

# Advanced defaultdict usage
def create_test_data_factory():
    """Фабрика для создания структурированных тестовых данных"""
    
    # Factory для тестовых пользователей
    user_factory = defaultdict(lambda: {
        "created_tests": [],
        "assigned_bugs": [],
        "execution_stats": {"passed": 0, "failed": 0, "skipped": 0}
    })
    
    # Добавляем данные
    test_assignments = [
        ("alice", "auth_login", "PASSED"),
        ("bob", "payment_process", "FAILED"),
        ("alice", "profile_update", "PASSED"),
        ("charlie", "search_function", "PASSED"),
        ("bob", "auth_logout", "PASSED"),
    ]
    
    for tester, test, status in test_assignments:
        user_factory[tester]["created_tests"].append(test)
        user_factory[tester]["execution_stats"][status.lower()] += 1
    
    return dict(user_factory)

def demonstrate_factory_usage():
    """Демонстрация использования фабрики"""
    
    factory_data = create_test_data_factory()
    
    print("📊 Статистика тестировщиков:")
    for tester, data in factory_data.items():
        stats = data["execution_stats"]
        total = sum(stats.values())
        pass_rate = (stats["passed"] / total) * 100 if total > 0 else 0
        
        print(f"  {tester}:")
        print(f"    Создано тестов: {len(data['created_tests'])}")
        print(f"    Успешных: {stats['passed']}")
        print(f"    Провалов: {stats['failed']}")
        print(f"    Пропущено: {stats['skipped']}")
        print(f"    Success rate: {pass_rate:.1f}%")
    
    return factory_data
```

### Deque - эффективные очереди для тестов

```python
from collections import deque
import time

def test_execution_queue():
    """Очередь выполнения тестов с deque"""
    
    # Создаем очередь тестов
    test_queue = deque([
        "test_user_login",
        "test_password_validation",
        "test_session_management",
        "test_user_logout"
    ])
    
    print("📋 Очередь тестов:")
    print(f"Всего тестов: {len(test_queue)}")
    print(f"Следующий тест: {test_queue[0]}")
    print(f"Последний тест: {test_queue[-1]}")
    
    # Выполняем тесты по очереди
    executed_tests = []
    while test_queue:
        current_test = test_queue.popleft()  # Быстрое извлечение слева
        print(f"Выполняем: {current_test}")
        executed_tests.append(current_test)
        time.sleep(0.1)  # Имитация выполнения
    
    print(f"✅ Выполнено тестов: {len(executed_tests)}")
    return executed_tests

# Сравнение производительности deque vs list
def benchmark_queue_performance():
    """Сравнение производительности очередей"""
    
    # Большой набор данных
    test_names = [f"test_{i:04d}" for i in range(10000)]
    
    # Тестирование list как очередь
    list_queue = list(test_names)
    start_time = time.time()
    
    while list_queue:
        list_queue.pop(0)  # Медленная операция для больших списков
    
    list_time = time.time() - start_time
    
    # Тестирование deque
    deque_queue = deque(test_names)
    start_time = time.time()
    
    while deque_queue:
        deque_queue.popleft()  # Быстрая операция O(1)
    
    deque_time = time.time() - start_time
    
    print(f"List queue time: {list_time:.4f} сек")
    print(f"Deque queue time: {deque_time:.4f} сек")
    print(f"Deque быстрее в {list_time/deque_time:.1f} раз")
    
    return list_time, deque_time

# Priority queue для тестов
def priority_test_execution():
    """Очередь выполнения тестов с приоритетами"""
    
    # Тесты с приоритетами (priority, test_name)
    priority_tests = deque([
        (1, "test_critical_security"),
        (3, "test_ui_components"),
        (2, "test_api_endpoints"),
        (1, "test_database_connections"),
        (3, "test_edge_cases")
    ])
    
    # Сортируем по приоритету
    priority_tests = deque(sorted(priority_tests, key=lambda x: x[0]))
    
    print("📋 Очередь тестов по приоритетам:")
    executed_order = []
    
    while priority_tests:
        priority, test_name = priority_tests.popleft()
        print(f"[Приоритет {priority}] Выполняем: {test_name}")
        executed_order.append(test_name)
    
    return executed_order
```

## 🎯 Named Tuples и Data Classes

### Named Tuples для структурированных тестовых данных

```python
from collections import namedtuple

# Определение структур данных
TestCase = namedtuple('TestCase', ['id', 'name', 'module', 'priority', 'steps', 'expected'])
TestResult = namedtuple('TestResult', ['test_case', 'status', 'execution_time', 'error_message'])

def create_test_suite():
    """Создание набора тестов с named tuples"""
    
    # Создаем тестовые случаи
    test_cases = [
        TestCase(
            id="TC001",
            name="User Login with Valid Credentials",
            module="Authentication",
            priority=1,
            steps=["Navigate to login page", "Enter valid credentials", "Click login button"],
            expected="User successfully logged in"
        ),
        TestCase(
            id="TC002",
            name="User Login with Invalid Password",
            module="Authentication",
            priority=2,
            steps=["Navigate to login page", "Enter valid username", "Enter invalid password"],
            expected="Error message displayed"
        )
    ]
    
    return test_cases

def execute_test_suite(test_cases):
    """Выполнение набора тестов"""
    
    results = []
    for test_case in test_cases:
        print(f"Выполняем: {test_case.name}")
        
        # Имитация выполнения теста
        import random
        status = random.choice(["PASSED", "FAILED"]) if "Invalid" in test_case.name else "PASSED"
        execution_time = random.uniform(0.5, 3.0)
        
        result = TestResult(
            test_case=test_case,
            status=status,
            execution_time=execution_time,
            error_message="Invalid credentials" if status == "FAILED" else None
        )
        
        results.append(result)
    
    return results

def analyze_test_results(results):
    """Анализ результатов тестирования"""
    
    print("📊 Результаты тестирования:")
    print(f"Всего тестов: {len(results)}")
    
    passed = [r for r in results if r.status == "PASSED"]
    failed = [r for r in results if r.status == "FAILED"]
    
    print(f"Успешно: {len(passed)}")
    print(f"Провалено: {len(failed)}")
    
    if failed:
        print("\n❌ Проваленные тесты:")
        for result in failed:
            print(f"  - {result.test_case.name}: {result.error_message}")
    
    # Статистика по времени выполнения
    avg_time = sum(r.execution_time for r in results) / len(results)
    print(f"\n⏱️  Среднее время выполнения: {avg_time:.2f} сек")
    
    return len(passed), len(failed), avg_time
```

### Data Classes для сложных структур

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import json

@dataclass
class TestConfiguration:
    """Конфигурация тестового окружения"""
    environment: str
    browser: str
    base_url: str
    timeout: int = 30
    headless: bool = True
    retry_attempts: int = 3

@dataclass
class TestSuite:
    """Набор тестов"""
    name: str
    module: str
    test_cases: List['TestCaseDC'] = field(default_factory=list)
    config: TestConfiguration = None

@dataclass
class TestCaseDC:
    """Тестовый случай (dataclass версия)"""
    id: str
    name: str
    description: str
    steps: List[str]
    expected_result: str
    priority: int = 1
    tags: List[str] = field(default_factory=list)
    preconditions: List[str] = field(default_factory=list)

@dataclass
class TestExecutionResult:
    """Результат выполнения теста"""
    test_case: TestCaseDC
    status: str
    execution_time: float
    timestamp: str
    error_message: Optional[str] = None
    screenshots: List[str] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)

def create_complex_test_structure():
    """Создание сложной структуры тестовых данных"""
    
    # Конфигурация
    config = TestConfiguration(
        environment="staging",
        browser="chrome",
        base_url="https://staging.example.com",
        timeout=45,
        headless=False
    )
    
    # Тестовые случаи
    login_test = TestCaseDC(
        id="AUTH-001",
        name="Successful User Login",
        description="Verify that users can login with valid credentials",
        steps=[
            "Navigate to login page",
            "Enter username 'testuser@example.com'",
            "Enter password 'password123'",
            "Click login button"
        ],
        expected_result="User redirected to dashboard",
        priority=1,
        tags=["authentication", "happy-path"],
        preconditions=["User account exists"]
    )
    
    # Набор тестов
    auth_suite = TestSuite(
        name="Authentication Tests",
        module="User Management",
        config=config
    )
    auth_suite.test_cases.append(login_test)
    
    return auth_suite

def serialize_test_data(test_suite):
    """Сериализация тестовых данных в JSON"""
    
    # Преобразование в словарь для сериализации
    def testcase_to_dict(tc):
        return {
            'id': tc.id,
            'name': tc.name,
            'description': tc.description,
            'steps': tc.steps,
            'expected_result': tc.expected_result,
            'priority': tc.priority,
            'tags': tc.tags,
            'preconditions': tc.preconditions
        }
    
    suite_dict = {
        'name': test_suite.name,
        'module': test_suite.module,
        'config': {
            'environment': test_suite.config.environment,
            'browser': test_suite.config.browser,
            'base_url': test_suite.config.base_url,
            'timeout': test_suite.config.timeout,
            'headless': test_suite.config.headless,
            'retry_attempts': test_suite.config.retry_attempts
        },
        'test_cases': [testcase_to_dict(tc) for tc in test_suite.test_cases]
    }
    
    return json.dumps(suite_dict, indent=2, ensure_ascii=False)

# Пример использования
def demonstrate_data_classes():
    """Демонстрация работы с data classes"""
    
    # Создаем структуру
    test_suite = create_complex_test_structure()
    
    # Сериализуем в JSON
    json_data = serialize_test_data(test_suite)
    print("📄 Сгенерированный JSON:")
    print(json_data)
    
    # Анализируем структуру
    print(f"\n📊 Статистика набора тестов:")
    print(f"Название: {test_suite.name}")
    print(f"Модуль: {test_suite.module}")
    print(f"Количество тестов: {len(test_suite.test_cases)}")
    print(f"Окружение: {test_suite.config.environment}")
    print(f"Браузер: {test_suite.config.browser}")
    
    return test_suite, json_data
```

## 📊 List Comprehensions для тестирования

### Основы list comprehensions в контексте тестирования

```python
def test_data_generation_comprehensions():
    """Генерация тестовых данных с comprehensions"""
    
    # ❌ Старый подход с циклами
    def old_approach():
        test_users = []
        for i in range(10):
            user = {
                'id': i,
                'username': f'user_{i:03d}',
                'email': f'user{i}@test.com',
                'is_active': i % 2 == 0
            }
            test_users.append(user)
        return test_users
    
    # ✅ Новый подход с comprehensions
    def new_approach():
        test_users = [
            {
                'id': i,
                'username': f'user_{i:03d}',
                'email': f'user{i}@test.com',
                'is_active': i % 2 == 0
            }
            for i in range(10)
        ]
        return test_users
    
    # Сравнение результатов
    old_result = old_approach()
    new_result = new_approach()
    
    assert old_result == new_result
    assert len(new_result) == 10
    assert new_result[0]['username'] == 'user_000'
    assert new_result[1]['is_active'] == False
    
    print("✅ List comprehensions работают корректно")
    return new_result

# Фильтрация тестовых данных
def filter_test_data():
    """Фильтрация тестовых данных с comprehensions"""
    
    # Тестовые данные
    test_results = [
        {'test': 'login', 'status': 'PASSED', 'module': 'auth'},
        {'test': 'logout', 'status': 'FAILED', 'module': 'auth'},
        {'test': 'payment', 'status': 'PASSED', 'module': 'commerce'},
        {'test': 'search', 'status': 'PASSED', 'module': 'ui'},
        {'test': 'profile', 'status': 'SKIPPED', 'module': 'user'},
    ]
    
    # Фильтрация проваленных тестов
    failed_tests = [test for test in test_results if test['status'] == 'FAILED']
    
    # Фильтрация по модулю
    auth_tests = [test for test in test_results if test['module'] == 'auth']
    
    # Комбинированная фильтрация
    active_tests = [test for test in test_results 
                   if test['status'] in ['PASSED', 'FAILED']]
    
    # Трансформация данных
    test_names = [test['test'] for test in test_results]
    status_report = [f"{test['test']}: {test['status']}" 
                    for test in test_results]
    
    print("📊 Результаты фильтрации:")
    print(f"Проваленные тесты: {len(failed_tests)}")
    print(f"Тесты аутентификации: {len(auth_tests)}")
    print(f"Активные тесты: {len(active_tests)}")
    print(f"Названия тестов: {test_names}")
    
    return failed_tests, auth_tests, active_tests, test_names, status_report

# Dictionary comprehensions для конфигураций
def config_comprehensions():
    """Работа с конфигурациями через comprehensions"""
    
    # Базовые конфигурации
    base_configs = {
        'dev': {'host': 'localhost', 'port': 8000, 'debug': True},
        'staging': {'host': 'staging.example.com', 'port': 80, 'debug': False},
        'prod': {'host': 'example.com', 'port': 443, 'debug': False}
    }
    
    # Добавляем общие параметры
    enhanced_configs = {
        env: {**config, 'timeout': 30, 'retries': 3}
        for env, config in base_configs.items()
    }
    
    # Фильтруем production конфигурации
    prod_configs = {
        env: config for env, config in enhanced_configs.items()
        if config['port'] in [80, 443]
    }
    
    # Генерируем URL из конфигураций
    urls = {
        env: f"https://{config['host']}:{config['port']}"
        for env, config in enhanced_configs.items()
    }
    
    print("🔧 Конфигурации:")
    for env, config in enhanced_configs.items():
        print(f"  {env}: {config}")
    
    print(f"\n🌐 URLs: {urls}")
    print(f"🔒 Production configs: {list(prod_configs.keys())}")
    
    return enhanced_configs, urls, prod_configs

# Set comprehensions для уникальных данных
def unique_test_data():
    """Работа с уникальными данными через set comprehensions"""
    
    # Тестовые данные с дубликатами
    test_modules = [
        'auth', 'payment', 'auth', 'ui', 'payment', 
        'search', 'auth', 'profile', 'ui'
    ]
    
    # Получаем уникальные модули
    unique_modules = {module for module in test_modules}
    
    # Анализируем дубликаты
    from collections import Counter
    module_counts = Counter(test_modules)
    duplicates = {module: count for module, count in module_counts.items() if count > 1}
    
    # Генерируем уникальные идентификаторы
    unique_ids = {f"id_{module}_{i}" 
                  for i, module in enumerate(test_modules)}
    
    print("📊 Анализ уникальности:")
    print(f"Исходные модули: {len(test_modules)}")
    print(f"Уникальные модули: {len(unique_modules)}")
    print(f"Уникальные модули: {sorted(unique_modules)}")
    print(f"Дубликаты: {duplicates}")
    print(f"Уникальные ID: {len(unique_ids)}")
    
    return unique_modules, duplicates, unique_ids
```

## 📁 Работа с файлами и сериализацией

### JSON для тестовых данных

```python
import json
from datetime import datetime

def manage_test_data_json():
    """Управление тестовыми данными в формате JSON"""
    
    # Структура тестовых данных
    test_data_structure = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "1.0",
            "author": "Test Team"
        },
        "test_suites": [
            {
                "suite_name": "Authentication Tests",
                "module": "User Management",
                "test_cases": [
                    {
                        "id": "AUTH-001",
                        "name": "Valid Login",
                        "description": "Test successful login with valid credentials",
                        "preconditions": ["User account exists"],
                        "steps": [
                            "Navigate to login page",
                            "Enter username 'testuser@test.com'",
                            "Enter password 'password123'",
                            "Click login button"
                        ],
                        "expected_result": "Redirect to dashboard",
                        "priority": 1,
                        "tags": ["authentication", "happy-path"]
                    },
                    {
                        "id": "AUTH-002",
                        "name": "Invalid Password",
                        "description": "Test login with invalid password",
                        "preconditions": ["User account exists"],
                        "steps": [
                            "Navigate to login page",
                            "Enter valid username",
                            "Enter invalid password",
                            "Click login button"
                        ],
                        "expected_result": "Error message displayed",
                        "priority": 2,
                        "tags": ["authentication", "error-handling"]
                    }
                ]
            }
        ]
    }
    
    # Сохраняем в файл
    with open('test_data.json', 'w', encoding='utf-8') as f:
        json.dump(test_data_structure, f, indent=2, ensure_ascii=False)
    
    # Читаем из файла
    with open('test_data.json', 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    
    # Проверки
    assert loaded_data['metadata']['version'] == '1.0'
    assert len(loaded_data['test_suites'][0]['test_cases']) == 2
    assert loaded_data['test_suites'][0]['suite_name'] == 'Authentication Tests'
    
    print("✅ JSON тестовые данные работают корректно")
    return loaded_data

# Работа с конфигурационными файлами
def config_file_management():
    """Управление конфигурационными файлами"""
    
    # Конфигурации для разных окружений
    configs = {
        "environments": {
            "development": {
                "base_url": "http://localhost:3000",
                "api_url": "http://localhost:8000/api",
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "test_db_dev"
                },
                "browser": "chrome",
                "headless": False,
                "timeout": 30
            },
            "staging": {
                "base_url": "https://staging.example.com",
                "api_url": "https://api-staging.example.com",
                "database": {
                    "host": "staging-db.example.com",
                    "port": 5432,
                    "name": "test_db_staging"
                },
                "browser": "chrome",
                "headless": True,
                "timeout": 45
            },
            "production": {
                "base_url": "https://example.com",
                "api_url": "https://api.example.com",
                "database": {
                    "host": "prod-db.example.com",
                    "port": 5432,
                    "name": "prod_db"
                },
                "browser": "chrome",
                "headless": True,
                "timeout": 60
            }
        },
        "test_settings": {
            "parallel_executors": 4,
            "retry_attempts": 3,
            "screenshot_on_failure": True,
            "video_recording": False
        }
    }
    
    # Сохраняем конфигурацию
    with open('test_config.json', 'w') as f:
        json.dump(configs, f, indent=2)
    
    # Загружаем и используем
    with open('test_config.json', 'r') as f:
        loaded_config = json.load(f)
    
    # Пример использования конфигурации
    current_env = "development"
    env_config = loaded_config['environments'][current_env]
    
    print(f"🔧 Конфигурация для {current_env}:")
    print(f"  Base URL: {env_config['base_url']}")
    print(f"  Database: {env_config['database']['host']}:{env_config['database']['port']}")
    print(f"  Timeout: {env_config['timeout']} сек")
    
    return loaded_config

# JSON Schema для валидации
def json_schema_validation():
    """Валидация тестовых данных по схеме"""
    
    # Простая схема для тестовых данных
    def validate_test_case(test_case):
        """Валидация структуры тестового случая"""
        
        required_fields = ['id', 'name', 'steps', 'expected_result']
        for field in required_fields:
            if field not in test_case:
                raise ValueError(f"Отсутствует обязательное поле: {field}")
        
        if not isinstance(test_case['steps'], list):
            raise ValueError("Поле 'steps' должно быть списком")
        
        if len(test_case['steps']) == 0:
            raise ValueError("Список шагов не может быть пустым")
        
        if 'priority' in test_case:
            if not isinstance(test_case['priority'], int) or test_case['priority'] < 1:
                raise ValueError("Приоритет должен быть положительным целым числом")
        
        return True
    
    # Тестовые данные
    valid_test_case = {
        "id": "TC001",
        "name": "Test Login",
        "steps": ["Open browser", "Navigate to site", "Enter credentials"],
        "expected_result": "Successful login",
        "priority": 1
    }
    
    invalid_test_case = {
        "name": "Test without ID",
        "steps": [],
        "expected_result": "Something"
    }
    
    # Валидация
    try:
        validate_test_case(valid_test_case)
        print("✅ Валидный тестовый случай прошел проверку")
    except ValueError as e:
        print(f"❌ Ошибка валидации: {e}")
    
    try:
        validate_test_case(invalid_test_case)
        print("❌ Невалидный тестовый случай неожиданно прошел проверку")
    except ValueError as e:
        print(f"✅ Невалидный тестовый случай корректно отклонен: {e}")
    
    return True
```

## 📈 Advanced Topics (по желанию)

### Pickle для сохранения состояний

```python
import pickle
from datetime import datetime

def state_preservation_example():
    """Пример сохранения состояния тестов"""
    
    # Сложная структура данных для сохранения
    test_state = {
        'session_id': 'sess_12345',
        'executed_tests': [
            {'name': 'test_login', 'status': 'PASSED', 'timestamp': datetime.now()},
            {'name': 'test_payment', 'status': 'FAILED', 'timestamp': datetime.now()}
        ],
        'current_user': {'username': 'testuser', 'permissions': ['read', 'write']},
        'environment_config': {'base_url': 'https://test.example.com', 'timeout': 30}
    }
    
    # Сохраняем состояние
    with open('test_state.pkl', 'wb') as f:
        pickle.dump(test_state, f)
    
    # Восстанавливаем состояние
    with open('test_state.pkl', 'rb') as f:
        restored_state = pickle.load(f)
    
    # Проверяем восстановление
    assert restored_state['session_id'] == test_state['session_id']
    assert len(restored_state['executed_tests']) == 2
    
    print("✅ Сохранение и восстановление состояния работает корректно")
    return restored_state

# XML обработка (для legacy систем)
def xml_processing_example():
    """Пример работы с XML (редко используется в современном тестировании)"""
    
    try:
        import xml.etree.ElementTree as ET
        
        # Создаем XML структуру тестовых данных
        root = ET.Element("testSuite")
        root.set("name", "Authentication Tests")
        
        test_case = ET.SubElement(root, "testCase")
        test_case.set("id", "XML-001")
        test_case.set("priority", "1")
        
        name = ET.SubElement(test_case, "name")
        name.text = "XML Login Test"
        
        steps = ET.SubElement(test_case, "steps")
        step1 = ET.SubElement(steps, "step")
        step1.text = "Navigate to login page"
        step2 = ET.SubElement(steps, "step")
        step2.text = "Enter credentials"
        
        # Преобразуем в строку
        xml_string = ET.tostring(root, encoding='unicode')
        print("📄 Сгенерированный XML:")
        print(xml_string)
        
        # Парсим обратно
        parsed_root = ET.fromstring(xml_string)
        assert parsed_root.get("name") == "Authentication Tests"
        assert len(parsed_root.findall(".//step")) == 2
        
        print("✅ XML обработка работает корректно")
        return xml_string
        
    except ImportError:
        print("⚠️  XML модуль недоступен")
        return None
```

## 🏠 Домашние задания

### Домашнее задание 8.1 (Базовое)
**Создать систему управления тестовыми данными**
- Использовать collections.Counter для анализа результатов
- Применить defaultdict для группировки тестов
- Реализовать deque для очереди выполнения тестов
- Написать тесты для всех компонентов

### Домашнее задание 8.2 (Среднее)
**Разработать фабрику тестовых данных**
- Создать named tuples для структурирования данных
- Реализовать data classes для сложных сущностей
- Использовать list comprehensions для генерации данных
- Сохранить данные в JSON файлы

### Домашнее задание 8.3 (Продвинутое)
**Построить полноценную систему конфигурации**
- Создать конфигурационные файлы для разных окружений
- Реализовать валидацию конфигураций
- Добавить сериализацию/десериализацию состояний
- Написать интеграционные тесты

## 📊 Тест знаний

**Промежуточный тест по модулю 8:**
- 15 вопросов по теории структур данных
- 5 практических заданий по работе с коллекциями
- 3 задания по генерации тестовых данных
- 2 задания по сериализации/десериализации
- Время выполнения: 75 минут
- Проходной балл: 80%

---
*Модуль 8 завершает фундаментальную подготовку по Python для автоматизации тестирования*