"""
🧪 Лабораторная работа 6.1: Настройка CI/CD Pipeline для автоматизированных тестов

🎯 Цель: Освоить настройку CI/CD pipelines для автоматизации тестирования

📚 Темы:
- GitLab CI/CD основы
- Docker для тестирования
- Pytest интеграция
- Отчеты и уведомления
- Оптимизация производительности

⏱️ Время выполнения: 120-150 минут

📝 Инструкции:
1. Выполните все задания по порядку
2. Используйте предоставленные шаблоны
3. Тестируйте изменения локально
4. Документируйте результаты
"""

import os
import subprocess
import yaml
import json
from pathlib import Path
import time

# =============================================================================
# ЗАДАНИЕ 1: Создание базового CI/CD pipeline
# =============================================================================

def create_gitlab_ci_yaml():
    """
    🎯 Задание: Создайте базовый .gitlab-ci.yml для тестирования Python проекта
    
    Сценарий: Настройте pipeline с 3 stages: build, test, deploy
    """
    
    # TODO: Создайте структуру CI/CD pipeline
    ci_config = {
        'stages': [
            'build',
            'test',
            'deploy'
        ],
        'variables': {
            'PYTHON_VERSION': '3.9',
            'PIP_CACHE_DIR': '$CI_PROJECT_DIR/.cache/pip'
        },
        'cache': {
            'key': '${CI_COMMIT_REF_SLUG}',
            'paths': [
                '.cache/pip/',
                'venv/'
            ]
        },
        'before_script': [
            'python --version',
            'pip install virtualenv',
            'virtualenv venv',
            'source venv/bin/activate',
            'pip install -r requirements.txt'
        ]
    }
    
    # TODO: Добавьте job для build stage
    ci_config['build_job'] = {
        'stage': 'build',
        'image': 'python:${PYTHON_VERSION}',
        'script': [
            'echo "Building application..."',
            'python setup.py build',
            'echo "Build completed successfully"'
        ],
        'artifacts': {
            'paths': ['dist/', 'build/'],
            'expire_in': '1 week'
        },
        'only': ['main', 'develop']
    }
    
    # TODO: Добавьте job для test stage
    ci_config['test_job'] = {
        'stage': 'test',
        'image': 'python:${PYTHON_VERSION}',
        'services': [
            'selenium/standalone-chrome:latest'
        ],
        'script': [
            'echo "Running tests..."',
            'pytest tests/ -v --tb=short --html=report.html --self-contained-html',
            'echo "Tests completed"'
        ],
        'artifacts': {
            'paths': ['report.html', 'screenshots/', 'allure-results/'],
            'when': 'always',
            'expire_in': '1 month'
        },
        'coverage': '/TOTAL.*?(\d+\.\d+)/',
        'only': ['main', 'develop', 'merge_requests']
    }
    
    # TODO: Добавьте job для deploy stage
    ci_config['deploy_job'] = {
        'stage': 'deploy',
        'image': 'python:${PYTHON_VERSION}',
        'script': [
            'echo "Deploying to staging environment..."',
            'echo "Deployment completed"',
            'echo "Running post-deployment tests..."',
            'pytest tests/smoke/ -v'
        ],
        'when': 'manual',
        'environment': 'staging',
        'only': ['main']
    }
    
    # Сохраняем конфигурацию
    with open('.gitlab-ci.yml', 'w') as f:
        yaml.dump(ci_config, f, default_flow_style=False, allow_unicode=True)
    
    print("✅ Базовый CI/CD pipeline создан в .gitlab-ci.yml")
    return ci_config

# =============================================================================
# ЗАДАНИЕ 2: Docker для тестирования
# =============================================================================

def create_test_dockerfiles():
    """
    🎯 Задание: Создайте Dockerfile для тестового окружения
    
    Сценарий: Подготовьте контейнер с всеми зависимостями для тестирования
    """
    
    # Dockerfile для тестового окружения
    dockerfile_content = """FROM python:3.9-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Установка Chrome для Selenium
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Установка chromedriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P ~/ && \
    unzip ~/chromedriver_linux64.zip -d ~/ && \
    rm ~/chromedriver_linux64.zip && \
    mv ~/chromedriver /usr/local/bin/chromedriver && \
    chmod +rx /usr/local/bin/chromedriver

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создание рабочей директории
WORKDIR /app

# Копирование исходного кода
COPY . .

# Установка прав доступа
RUN chmod +x ./scripts/test_runner.sh

# Проверка установки
RUN python -c "import pytest; import selenium; print('Dependencies installed successfully')"

CMD ["pytest", "tests/", "-v"]
"""
    
    with open('Dockerfile.test', 'w') as f:
        f.write(dockerfile_content)
    
    # docker-compose для тестового окружения
    compose_content = """version: '3.8'

services:
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    volumes:
      - .:/app
      - test-reports:/app/reports
    environment:
      - DISPLAY=:99
      - SELENIUM_HOST=selenium-hub
    depends_on:
      - selenium-hub
      - chrome-node
    networks:
      - test-network

  selenium-hub:
    image: selenium/hub:latest
    ports:
      - "4444:4444"
    networks:
      - test-network

  chrome-node:
    image: selenium/node-chrome:latest
    environment:
      - HUB_HOST=selenium-hub
      - NODE_MAX_INSTANCES=2
      - NODE_MAX_SESSION=2
    depends_on:
      - selenium-hub
    networks:
      - test-network

volumes:
  test-reports:

networks:
  test-network:
    driver: bridge
"""
    
    with open('docker-compose.test.yml', 'w') as f:
        f.write(compose_content)
    
    print("✅ Docker файлы созданы: Dockerfile.test, docker-compose.test.yml")
    return dockerfile_content, compose_content

# =============================================================================
# ЗАДАНИЕ 3: Pytest интеграция с CI/CD
# =============================================================================

def create_pytest_ci_integration():
    """
    🎯 Задание: Настройте pytest для CI/CD окружения
    
    Сценарий: Создайте конфигурацию pytest с поддержкой CI переменных
    """
    
    # pytest.ini для CI
    pytest_ini_content = """[tool:pytest]
# CI/CD специфичные настройки
addopts = 
    -v 
    --tb=short 
    --strict-markers
    --strict-config
    --continue-on-collection-errors
    --cache-clear
    --durations=10
    --color=yes

# Параметры для CI
markers =
    smoke: Smoke tests for CI
    regression: Regression tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    critical: Critical functionality tests

# Пути к тестам
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Исключения
norecursedirs = 
    .git
    .tox
    .eggs
    dist
    build
    venv
    node_modules

# Фильтры предупреждений
filterwarnings =
    ignore::DeprecationWarning
    error::UserWarning

[coverage:run]
source = src/
omit = 
    */venv/*
    */tests/*
    */setup.py

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

"""
    
    with open('pytest.ini', 'w') as f:
        f.write(pytest_ini_content)
    
    # conftest.py для CI
    conftest_content = '''import pytest
import os
import tempfile
from datetime import datetime

def pytest_configure(config):
    """Конфигурация pytest для CI окружения"""
    
    # Установка CI специфичных настроек
    if os.getenv('CI'):
        # Установка таймаутов для CI
        config.option.timeout = 300  # 5 минут на тест в CI
        
        # Установка количества worker для pytest-xdist
        if not config.option.numprocesses:
            config.option.numprocesses = 2  # Ограничение для CI
    
    # Добавление меток для CI
    config.addinivalue_line(
        "markers", "ci: mark test to run in CI environment"
    )
    config.addinivalue_line(
        "markers", "slow_ci: mark slow test for CI"
    )

@pytest.fixture(scope="session")
def ci_environment():
    """Фикстура для CI окружения"""
    return {
        'is_ci': os.getenv('CI', False),
        'branch': os.getenv('CI_COMMIT_REF_NAME', 'local'),
        'commit_sha': os.getenv('CI_COMMIT_SHA', 'unknown'),
        'pipeline_id': os.getenv('CI_PIPELINE_ID', 'local'),
        'runner_tags': os.getenv('CI_RUNNER_TAGS', '').split(','),
        'build_dir': os.getenv('CI_PROJECT_DIR', './')
    }

@pytest.fixture(scope="session")
def test_report_dir(ci_environment):
    """Фикстура для директории отчетов"""
    if ci_environment['is_ci']:
        report_dir = f"ci_reports/{ci_environment['pipeline_id']}"
    else:
        report_dir = f"local_reports/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    os.makedirs(report_dir, exist_ok=True)
    return report_dir

@pytest.fixture(autouse=True)
def test_metadata(request, ci_environment):
    """Фикстура для метаданных теста"""
    test_start = datetime.now()
    
    # Логирование начала теста
    if ci_environment['is_ci']:
        print(f"\\n=== STARTING TEST: {request.node.name} ===")
        print(f"Branch: {ci_environment['branch']}")
        print(f"Commit: {ci_environment['commit_sha'][:8]}")
    
    yield
    
    # Логирование завершения теста
    duration = (datetime.now() - test_start).total_seconds()
    if ci_environment['is_ci']:
        print(f"=== FINISHED TEST: {request.node.name} (Duration: {duration:.2f}s) ===")

# Hook для CI отчетности
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook для генерации CI отчетов"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Логирование падений в CI
        if os.getenv('CI'):
            print(f"\\n❌ TEST FAILED: {item.nodeid}")
            print(f"Duration: {getattr(rep, 'duration', 'unknown')}s")
            
            # Дополнительная диагностика в CI
            if hasattr(item, 'funcargs'):
                print("Function arguments:", item.funcargs)
'''
    
    with open('conftest.py', 'w') as f:
        f.write(conftest_content)
    
    print("✅ Pytest интеграция создана: pytest.ini, conftest.py")
    return pytest_ini_content, conftest_content

# =============================================================================
# ЗАДАНИЕ 4: Настройка отчетов и уведомлений
# =============================================================================

def create_reporting_setup():
    """
    🎯 Задание: Настройте генерацию отчетов и уведомлений
    
    Сценарий: Создайте систему отчетности для CI/CD pipeline
    """
    
    # Скрипт генерации отчетов
    report_script = '''#!/bin/bash
# Скрипт генерации отчетов для CI

set -e

echo "📊 Generating test reports..."

# Убедимся, что директории существуют
mkdir -p reports/allure reports/html reports/json

# Генерация HTML отчета
if command -v pytest &> /dev/null; then
    echo "Generating HTML report..."
    pytest tests/ --html=reports/html/report.html --self-contained-html --tb=short
fi

# Генерация Allure отчета
if command -v allure &> /dev/null; then
    echo "Generating Allure report..."
    allure generate allure-results/ -o reports/allure/ --clean
fi

# Генерация JSON отчета
if command -v pytest &> /dev/null; then
    echo "Generating JSON report..."
    pytest tests/ --json-report --json-report-file=reports/json/results.json
fi

# Сбор метрик покрытия
if command -v coverage &> /dev/null; then
    echo "Generating coverage report..."
    coverage run -m pytest tests/
    coverage report -m > reports/coverage.txt
    coverage html -d reports/coverage_html/
fi

echo "✅ Reports generated successfully"
echo "📁 Report directory contents:"
ls -la reports/

# Проверка результатов
FAILURES=$(find reports/ -name "*.html" -exec grep -l "FAILED\\|ERROR" {} \\; | wc -l)
if [ $FAILURES -gt 0 ]; then
    echo "⚠️  Found $FAILURES failing test reports"
    exit 1
else
    echo "✅ All tests passed"
fi
'''
    
    with open('scripts/generate_reports.sh', 'w') as f:
        f.write(report_script)
    
    # Make executable
    os.chmod('scripts/generate_reports.sh', 0o755)
    
    # Конфигурация уведомлений
    notification_config = {
        "notifications": {
            "on_success": {
                "channels": ["#ci-cd", "#qa-team"],
                "template": "✅ Pipeline {pipeline_id} succeeded in {duration}s",
                "include": ["test_results", "coverage", "performance"]
            },
            "on_failure": {
                "channels": ["#ci-cd", "#alerts"],
                "template": "❌ Pipeline {pipeline_id} failed after {duration}s",
                "include": ["failed_tests", "error_logs", "committer_info"],
                "escalation": {
                    "after_minutes": 15,
                    "to": ["qa_lead", "devops_engineer"]
                }
            },
            "on_manual_action": {
                "channels": ["#deployment"],
                "template": "🚀 Deployment to {environment} initiated by {user}"
            }
        },
        "metrics": {
            "track": [
                "pipeline_duration",
                "test_execution_time", 
                "test_pass_rate",
                "code_coverage",
                "flaky_test_rate",
                "deployment_success_rate"
            ],
            "thresholds": {
                "min_pass_rate": 95.0,
                "min_coverage": 80.0,
                "max_flaky_rate": 5.0,
                "max_pipeline_duration": 600  # 10 minutes
            }
        }
    }
    
    with open('notification_config.json', 'w') as f:
        json.dump(notification_config, f, indent=2)
    
    print("✅ Система отчетности создана: scripts/generate_reports.sh, notification_config.json")
    return report_script, notification_config

# =============================================================================
# ЗАДАНИЕ 5: Оптимизация производительности
# =============================================================================

def create_performance_optimization():
    """
    🎯 Задание: Настройте оптимизацию производительности CI/CD
    
    Сценарий: Создайте конфигурации для ускорения выполнения тестов
    """
    
    # Матрица тестов для параллельного выполнения
    test_matrix_config = {
        "test_suites": {
            "smoke_tests": {
                "path": "tests/smoke/",
                "parallel_jobs": 2,
                "timeout": 300,
                "critical": True
            },
            "regression_tests": {
                "path": "tests/regression/",
                "parallel_jobs": 4,
                "timeout": 1800,
                "critical": False
            },
            "integration_tests": {
                "path": "tests/integration/",
                "parallel_jobs": 3,
                "timeout": 1200,
                "critical": True
            },
            "api_tests": {
                "path": "tests/api/",
                "parallel_jobs": 2,
                "timeout": 600,
                "critical": True
            }
        },
        "optimization_settings": {
            "cache_dependencies": True,
            "reuse_volumes": True,
            "smart_retry": {
                "enabled": True,
                "max_attempts": 2,
                "only_flaky": True
            },
            "resource_limits": {
                "cpu": "2",
                "memory": "4G",
                "concurrency": 4
            },
            "early_exit": {
                "enabled": True,
                "failure_threshold": 5
            }
        }
    }
    
    with open('test_matrix.json', 'w') as f:
        json.dump(test_matrix_config, f, indent=2)
    
    # Скрипт оптимизации
    optimization_script = '''#!/bin/bash
# Скрипт оптимизации производительности CI

set -e

echo "⚡ Optimizing CI performance..."

# Кэширование зависимостей
if [ -f "requirements.txt" ]; then
    echo "Caching Python packages..."
    pip install --user --no-cache-dir -r requirements.txt
fi

# Определение измененных файлов (для incremental testing)
if [ ! -z "$CI_COMMIT_BEFORE_SHA" ]; then
    echo "Detecting changed files..."
    git diff --name-only $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA > changed_files.txt
fi

# Установка переменных производительности
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PIP_NO_CACHE_DIR=1

# Настройка pytest для параллельного выполнения
export PYTEST_XDIST_AUTO_NUM_WORKERS=auto

# Лимиты ресурсов
ulimit -n 4096  # увеличение лимита файловых дескрипторов

echo "✅ Performance optimizations applied"
echo "🔧 Current settings:"
echo "  PYTHONUNBUFFERED=$PYTHONUNBUFFERED"
echo "  PYTHONDONTWRITEBYTECODE=$PYTHONDONTWRITEBYTECODE"
echo "  Concurrency: $(nproc) cores available"
'''
    
    with open('scripts/optimize_ci.sh', 'w') as f:
        f.write(optimization_script)
    
    # Make executable
    os.chmod('scripts/optimize_ci.sh', 0o755)
    
    print("✅ Оптимизация производительности создана: test_matrix.json, scripts/optimize_ci.sh")
    return test_matrix_config, optimization_script

# =============================================================================
# ЗАДАНИЕ 6: Интеграционное задание - Полный CI/CD Pipeline
# =============================================================================

def create_complete_ci_cd_setup():
    """
    🎯 Задание: Создайте полный CI/CD setup для тестирования
    
    Сценарий: Объедините все компоненты в рабочий pipeline
    """
    
    print("🚀 Создание полного CI/CD setup...")
    
    # Создаем необходимые директории
    dirs_to_create = [
        'scripts/',
        'reports/',
        'tests/unit/',
        'tests/integration/',
        'tests/e2e/',
        'tests/smoke/',
        'config/',
        'docs/ci_cd/'
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Создаем базовый тест для проверки
    basic_test = '''import pytest
import os

def test_ci_environment():
    """Тест проверки CI окружения"""
    # Проверяем наличие CI переменных
    assert "pytest" in repr(globals())
    
    # Проверяем доступ к директориям
    assert os.path.exists("reports/")
    
    # Простой функциональный тест
    assert 1 + 1 == 2
    print("✅ CI environment test passed")

@pytest.mark.smoke
def test_smoke_functionality():
    """Smoke тест для проверки базовой функциональности"""
    result = "hello world"
    assert "hello" in result
    assert len(result) > 0
    print("✅ Smoke test passed")

@pytest.mark.integration
def test_integration_placeholder():
    """Placeholder для интеграционного теста"""
    # В реальном проекте здесь будет интеграционный тест
    assert True  # Заменить на реальную логику
    print("✅ Integration test placeholder passed")
'''
    
    with open('tests/smoke/test_basic_ci.py', 'w') as f:
        f.write(basic_test)
    
    # Создаем requirements.txt для тестов
    requirements = '''pytest>=7.0.0
pytest-html>=3.1.0
pytest-xdist>=2.5.0
pytest-cov>=3.0.0
allure-pytest>=2.10.0
selenium>=4.0.0
requests>=2.28.0
docker>=6.0.0
pyyaml>=6.0
jsonschema>=4.0.0
coverage>=6.0.0
'''
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ Полный CI/CD setup создан!")
    print("\\n📋 Созданные компоненты:")
    print("  • .gitlab-ci.yml - основной pipeline")
    print("  • Dockerfile.test - тестовое окружение")
    print("  • docker-compose.test.yml - мультиконтейнерное окружение") 
    print("  • pytest.ini - конфигурация pytest")
    print("  • conftest.py - CI специфичные фикстуры")
    print("  • scripts/generate_reports.sh - генерация отчетов")
    print("  • scripts/optimize_ci.sh - оптимизация производительности")
    print("  • test_matrix.json - матрица тестов")
    print("  • notification_config.json - конфигурация уведомлений")
    print("  • Базовые тесты в tests/smoke/")
    
    return True

# =============================================================================
# Функция запуска всех заданий
# =============================================================================

def run_all_labs():
    """Запускает все задания лабораторной работы"""
    print("🔬 Запуск лабораторной работы 6.1: CI/CD Pipeline Setup")
    print("=" * 80)
    
    try:
        print("\\n1️⃣ Создание базового CI/CD pipeline...")
        ci_config = create_gitlab_ci_yaml()
        
        print("\\n2️⃣ Создание Docker файлов...")
        docker_content, compose_content = create_test_dockerfiles()
        
        print("\\n3️⃣ Настройка Pytest интеграции...")
        pytest_ini, conftest = create_pytest_ci_integration()
        
        print("\\n4️⃣ Настройка отчетности...")
        report_script, notification_config = create_reporting_setup()
        
        print("\\n5️⃣ Настройка оптимизации...")
        matrix_config, opt_script = create_performance_optimization()
        
        print("\\n6️⃣ Создание полного CI/CD setup...")
        complete_setup = create_complete_ci_cd_setup()
        
        print("\\n" + "=" * 80)
        print("🎉 Лабораторная работа 6.1 завершена успешно!")
        print("🏆 Вы создали полноценный CI/CD pipeline для автоматизированного тестирования!")
        
        print("\\n📋 Сгенерированные файлы:")
        generated_files = [
            '.gitlab-ci.yml',
            'Dockerfile.test', 
            'docker-compose.test.yml',
            'pytest.ini',
            'conftest.py',
            'scripts/generate_reports.sh',
            'scripts/optimize_ci.sh',
            'test_matrix.json',
            'notification_config.json',
            'requirements.txt',
            'tests/smoke/test_basic_ci.py'
        ]
        
        for file in generated_files:
            status = "✅" if Path(file).exists() else "❌"
            print(f"  {status} {file}")
        
        print("\\n💡 Следующие шаги:")
        print("  1. Проверьте сгенерированные файлы на соответствие вашему проекту")
        print("  2. Настройте GitLab CI/CD variables")
        print("  3. Протестируйте pipeline в ветке feature")
        print("  4. Доработайте тесты под ваш конкретный проект")
        
        return True
        
    except Exception as e:
        print(f"\\n❌ Ошибка при выполнении лабораторной работы: {e}")
        import traceback
        traceback.print_exc()
        return False

# Запуск при импорте как модуля
if __name__ == "__main__":
    success = run_all_labs()
    if success:
        print("\\n🎉 Поздравляем! Вы успешно завершили лабораторную работу по CI/CD!")
    else:
        print("\\n⚠️  Работа завершена с ошибками. Проверьте логи выше.")