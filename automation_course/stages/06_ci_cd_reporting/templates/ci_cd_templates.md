# CI/CD и отчетность - Шаблоны

## 1. GitLab CI Templates

### .gitlab-ci.yml (базовый шаблон)

```yaml
# .gitlab-ci.yml - Базовый шаблон CI/CD pipeline
stages:
  - build
  - test
  - deploy
  - report

variables:
  # Базовые переменные
  PYTHON_VERSION: "3.9"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  TEST_REPORTS_DIR: "$CI_PROJECT_DIR/reports"
  ALLURE_RESULTS_DIR: "$CI_PROJECT_DIR/allure-results"

# Кэширование зависимостей
cache:
  key: "${CI_COMMIT_REF_SLUG}"
  paths:
    - .cache/pip/
    - venv/
    - node_modules/

# Общие скрипты перед выполнением
before_script:
  - python --version
  - pip install virtualenv
  - virtualenv venv
  - source venv/bin/activate
  - pip install -r requirements.txt

# Build stage
build_job:
  stage: build
  image: python:${PYTHON_VERSION}
  script:
    - echo "📦 Building application..."
    - python setup.py build
    - echo "✅ Build completed successfully"
  artifacts:
    paths:
      - dist/
      - build/
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests

# Test stage - Unit tests
unit_tests:
  stage: test
  image: python:${PYTHON_VERSION}
  script:
    - echo "🧪 Running unit tests..."
    - pytest tests/unit/ -v --tb=short --cov=src --cov-report=html:reports/coverage
    - echo "✅ Unit tests completed"
  artifacts:
    paths:
      - reports/
      - coverage.xml
      - htmlcov/
    when: always
    expire_in: 1 month
  coverage: '/TOTAL.*?(\d+\.\d+)/'
  only:
    - main
    - develop
    - merge_requests

# Test stage - Integration tests
integration_tests:
  stage: test
  image: python:${PYTHON_VERSION}
  services:
    - name: selenium/standalone-chrome:latest
      alias: selenium
  variables:
    SELENIUM_URL: "http://selenium:4444/wd/hub"
  script:
    - echo "🔍 Running integration tests..."
    - pytest tests/integration/ -v --tb=short --html=reports/integration_report.html
    - echo "✅ Integration tests completed"
  artifacts:
    paths:
      - reports/integration_report.html
      - screenshots/
    when: on_failure
    expire_in: 1 week
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
  only:
    - main
    - develop

# Test stage - E2E tests
e2e_tests:
  stage: test
  image: python:${PYTHON_VERSION}
  services:
    - selenium/standalone-chrome:latest
  script:
    - echo "🌐 Running end-to-end tests..."
    - pytest tests/e2e/ -v --tb=short --alluredir=allure-results/
    - echo "✅ E2E tests completed"
  artifacts:
    paths:
      - allure-results/
    when: always
    expire_in: 2 weeks
  dependencies:
    - build_job
  only:
    - main

# Deploy stage
deploy_staging:
  stage: deploy
  image: python:${PYTHON_VERSION}
  script:
    - echo "🚀 Deploying to staging environment..."
    - echo "Branch: ${CI_COMMIT_REF_NAME}"
    - echo "Commit: ${CI_COMMIT_SHORT_SHA}"
    - echo "Pipeline: ${CI_PIPELINE_ID}"
    - echo "Deploying application..."
    - echo "✅ Deployment completed"
    - echo "🔍 Running post-deployment tests..."
    - pytest tests/smoke/ -v --tb=short
  when: manual
  environment:
    name: staging
    url: https://staging.your-app.com
  only:
    - main
  except:
    - schedules

# Report stage
generate_reports:
  stage: report
  image: python:${PYTHON_VERSION}
  script:
    - echo "📊 Generating comprehensive reports..."
    - pip install allure-pytest
    - allure generate allure-results/ -o reports/allure/ --clean
    - echo "✅ Reports generated in reports/ directory"
  artifacts:
    paths:
      - reports/
    expire_in: 1 month
  dependencies:
    - e2e_tests
  only:
    - main
    - schedules

# Security scan
security_scan:
  stage: test
  image: registry.gitlab.com/gitlab-org/security-products/sast:latest
  variables:
    SAST_CONFIDENCE_LEVEL: 3
  allow_failure: true
  only:
    - main
    - develop
```

## 2. Docker Templates

### Dockerfile.test (тестовое окружение)

```dockerfile
# Dockerfile.test - Окружение для тестирования
FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Установка ChromeDriver
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

# Создание директорий для отчетов
RUN mkdir -p reports screenshots allure-results

# Установка прав доступа
RUN chmod +x ./scripts/test_runner.sh

# Проверка установки
RUN python -c "import pytest; import selenium; import requests; print('Dependencies installed successfully')"

# Дефолтная команда
CMD ["pytest", "tests/", "-v"]
```

### docker-compose.test.yml (мультиконтейнерное тестирование)

```yaml
# docker-compose.test.yml - Мультиконтейнерное тестовое окружение
version: '3.8'

services:
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    container_name: test-runner
    volumes:
      - .:/app
      - test-reports:/app/reports
      - screenshots-volume:/app/screenshots
    environment:
      - DISPLAY=:99
      - SELENIUM_HOST=selenium-hub
      - CHROME_HEADLESS=true
      - PYTEST_ADDOPTS="--tb=short -v"
    depends_on:
      - selenium-hub
      - chrome-node
    networks:
      - test-network
    command: >
      bash -c "
        echo 'Starting tests...' &&
        pytest tests/ -v --tb=short --html=reports/report.html --self-contained-html
      "

  selenium-hub:
    image: selenium/hub:latest
    container_name: selenium-hub
    ports:
      - "4444:4444"
    environment:
      - GRID_MAX_SESSION=6
      - GRID_BROWSER_TIMEOUT=30000
      - GRID_TIMEOUT=30000
    networks:
      - test-network

  chrome-node:
    image: selenium/node-chrome:latest
    container_name: chrome-node
    environment:
      - HUB_HOST=selenium-hub
      - NODE_MAX_INSTANCES=2
      - NODE_MAX_SESSION=2
      - SCREEN_WIDTH=1920
      - SCREEN_HEIGHT=1080
    depends_on:
      - selenium-hub
    networks:
      - test-network
    shm_size: 2gb

  postgres-test:
    image: postgres:13-alpine
    container_name: postgres-test
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    ports:
      - "5433:5432"
    networks:
      - test-network

  redis-test:
    image: redis:alpine
    container_name: redis-test
    ports:
      - "6380:6379"
    networks:
      - test-network

volumes:
  test-reports:
    driver: local
  screenshots-volume:
    driver: local

networks:
  test-network:
    driver: bridge
```

## 3. Pytest Configuration Templates

### pytest.ini (основная конфигурация)

```ini
[tool:pytest]
# Основные настройки для CI/CD
addopts = 
    -v 
    --tb=short 
    --strict-markers
    --strict-config
    --continue-on-collection-errors
    --cache-clear
    --durations=10
    --color=yes
    --junit-xml=reports/junit.xml

# Маркеры для различных типов тестов
markers =
    smoke: Smoke tests for CI
    regression: Regression tests
    integration: Integration tests
    e2e: End-to-end tests
    api: API tests
    ui: UI tests
    slow: Slow running tests
    critical: Critical functionality tests
    performance: Performance tests
    security: Security tests

# Пути к тестам
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Исключения из рекурсивного поиска
norecursedirs = 
    .git
    .tox
    .eggs
    dist
    build
    venv
    node_modules
    .cache
    __pycache__

# Фильтры предупреждений
filterwarnings =
    ignore::DeprecationWarning
    ignore::ResourceWarning
    error::UserWarning

[coverage:run]
source = src/
omit = 
    */venv/*
    */tests/*
    */setup.py
    */conftest.py

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

[coverage:html]
directory = reports/coverage_html
```

### conftest.py (фикстуры для CI)

```python
# conftest.py - CI/CD специфичные фикстуры
import pytest
import os
import tempfile
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
        'runner_tags': os.getenv('CI_RUNNER_TAGS', '').split(',') if os.getenv('CI_RUNNER_TAGS') else [],
        'build_dir': os.getenv('CI_PROJECT_DIR', './'),
        'job_name': os.getenv('CI_JOB_NAME', 'local'),
        'job_id': os.getenv('CI_JOB_ID', 'local')
    }

@pytest.fixture(scope="session")
def test_report_dir(ci_environment):
    """Фикстура для директории отчетов"""
    if ci_environment['is_ci']:
        report_dir = f"ci_reports/{ci_environment['pipeline_id']}/{ci_environment['job_name']}"
    else:
        report_dir = f"local_reports/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    os.makedirs(report_dir, exist_ok=True)
    return report_dir

@pytest.fixture(scope="session")
def selenium_driver(ci_environment):
    """Фикстура для Selenium WebDriver"""
    if ci_environment['is_ci']:
        # Использовать remote driver для CI
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        driver = webdriver.Remote(
            command_executor=os.getenv('SELENIUM_URL', 'http://selenium-hub:4444/wd/hub'),
            options=options
        )
    else:
        # Использовать local driver для локальной разработки
        options = Options()
        if os.getenv('HEADLESS', 'false').lower() == 'true':
            options.add_argument('--headless')
        
        driver = webdriver.Chrome(options=options)
    
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def test_metadata(request, ci_environment):
    """Фикстура для метаданных теста"""
    test_start = datetime.now()
    
    # Логирование начала теста
    if ci_environment['is_ci']:
        print(f"\n=== STARTING TEST: {request.node.name} ===")
        print(f"Branch: {ci_environment['branch']}")
        print(f"Commit: {ci_environment['commit_sha'][:8]}")
        print(f"Pipeline: {ci_environment['pipeline_id']}")
        print(f"Job: {ci_environment['job_name']}")
    
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
            print(f"\n❌ TEST FAILED: {item.nodeid}")
            print(f"Duration: {getattr(rep, 'duration', 'unknown')}s")
            
            # Дополнительная диагностика в CI
            if hasattr(item, 'funcargs'):
                print("Function arguments:", item.funcargs)
```

## 4. Reporting Templates

### notification_config.json (конфигурация уведомлений)

```json
{
  "notifications": {
    "on_success": {
      "channels": ["#ci-cd", "#qa-team"],
      "template": "✅ Pipeline {pipeline_id} succeeded in {duration}s",
      "include": ["test_results", "coverage", "performance"],
      "webhook": {
        "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
        "method": "POST"
      }
    },
    "on_failure": {
      "channels": ["#ci-cd", "#alerts", "#dev-team"],
      "template": "❌ Pipeline {pipeline_id} failed after {duration}s",
      "include": ["failed_tests", "error_logs", "committer_info"],
      "escalation": {
        "after_minutes": 15,
        "to": ["qa_lead", "devops_engineer", "team_lead"],
        "message": "Pipeline failure requires immediate attention"
      },
      "webhook": {
        "url": "https://hooks.slack.com/services/YOUR/FAILURE/WEBHOOK",
        "method": "POST"
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
      "deployment_success_rate",
      "mean_time_to_detection",
      "mean_time_to_recovery"
    ],
    "thresholds": {
      "min_pass_rate": 95.0,
      "min_coverage": 80.0,
      "max_flaky_rate": 5.0,
      "max_pipeline_duration": 600,
      "max_test_execution_time": 300
    }
  },
  "reporting": {
    "formats": ["html", "json", "junit", "allure"],
    "retention_days": 30,
    "archive_failed_builds": true
  }
}
```

### grafana-dashboard-template.json (шаблон Grafana dashboard)

```json
{
  "dashboard": {
    "id": null,
    "title": "Test Automation Metrics",
    "tags": ["tests", "ci", "quality"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Test Pass Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "avg(test_pass_rate)",
            "legendFormat": "Pass Rate"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "min": 0,
            "max": 100
          }
        }
      },
      {
        "id": 2,
        "title": "Pipeline Duration",
        "type": "graph",
        "targets": [
          {
            "expr": "pipeline_duration_seconds",
            "legendFormat": "Duration"
          }
        ]
      },
      {
        "id": 3,
        "title": "Failed Tests Over Time",
        "type": "graph",
        "targets": [
          {
            "expr": "failed_tests_count",
            "legendFormat": "Failed Tests"
          }
        ]
      }
    ],
    "time": {
      "from": "now-24h",
      "to": "now"
    }
  }
}
```

## 5. Script Templates

### scripts/generate_reports.sh (генерация отчетов)

```bash
#!/bin/bash
# scripts/generate_reports.sh - Генерация отчетов для CI

set -e

echo "📊 Generating test reports..."

# Убедимся, что директории существуют
mkdir -p reports/allure reports/html reports/json reports/coverage

# Проверка наличия необходимых инструментов
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest is not installed"
    exit 1
fi

# Генерация HTML отчета
echo "Generating HTML report..."
pytest tests/ --html=reports/html/report.html --self-contained-html --tb=short

# Генерация JUnit XML для CI систем
echo "Generating JUnit report..."
pytest tests/ --junitxml=reports/junit.xml

# Генерация Allure отчета
if command -v allure &> /dev/null; then
    echo "Generating Allure report..."
    allure generate allure-results/ -o reports/allure/ --clean
else
    echo "⚠️  Allure is not installed, skipping Allure report"
fi

# Генерация JSON отчета
echo "Generating JSON report..."
pip install pytest-json-report
pytest tests/ --json-report --json-report-file=reports/json/results.json

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

# Подсчет результатов
TOTAL_TESTS=$(grep -c "test" reports/junit.xml 2>/dev/null || echo "0")
PASSED_TESTS=$(grep -c "status=\"passed\"" reports/junit.xml 2>/dev/null || echo "0")
FAILED_TESTS=$(grep -c "status=\"failed\"" reports/junit.xml 2>/dev/null || echo "0")

echo "📈 Test Results:"
echo "  Total: $TOTAL_TESTS"
echo "  Passed: $PASSED_TESTS"
echo "  Failed: $FAILED_TESTS"

# Проверка результатов
if [ $FAILED_TESTS -gt 0 ]; then
    echo "❌ Tests failed: $FAILED_TESTS tests failed"
    exit 1
else
    echo "✅ All tests passed"
fi
```

### scripts/optimize_ci.sh (оптимизация CI)

```bash
#!/bin/bash
# scripts/optimize_ci.sh - Оптимизация производительности CI

set -e

echo "⚡ Optimizing CI performance..."

# Кэширование зависимостей
if [ -f "requirements.txt" ]; then
    echo "Caching Python packages..."
    pip install --user --no-cache-dir -r requirements.txt
fi

# Определение измененных файлов (для incremental testing)
if [ ! -z "$CI_COMMIT_BEFORE_SHA" ] && [ "$CI_COMMIT_BEFORE_SHA" != "0000000000000000000000000000000000000000" ]; then
    echo "Detecting changed files..."
    git diff --name-only $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA > changed_files.txt
    echo "Changed files:"
    cat changed_files.txt
fi

# Установка переменных производительности
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PIP_NO_CACHE_DIR=1

# Настройка pytest для параллельного выполнения
if command -v pytest &> /dev/null; then
    export PYTEST_XDIST_AUTO_NUM_WORKERS=auto
    echo "Pytest parallel workers: $PYTEST_XDIST_AUTO_NUM_WORKERS"
fi

# Лимиты ресурсов
ulimit -n 4096  # увеличение лимита файловых дескрипторов

# Оптимизация Docker
if command -v docker &> /dev/null; then
    echo "Optimizing Docker..."
    docker system prune -f
    docker volume prune -f
fi

echo "✅ Performance optimizations applied"
echo "🔧 Current settings:"
echo "  PYTHONUNBUFFERED=$PYTHONUNBUFFERED"
echo "  PYTHONDONTWRITEBYTECODE=$PYTHONDONTWRITEBYTECODE"
echo "  Concurrency: $(nproc) cores available"
echo "  Memory: $(free -m | awk 'NR==2{print $2}') MB"
```

## 6. Test Matrix Template

### test_matrix.json (матрица тестов)

```json
{
  "test_suites": {
    "smoke_tests": {
      "path": "tests/smoke/",
      "parallel_jobs": 2,
      "timeout": 300,
      "critical": true,
      "schedule": "every_day",
      "environments": ["staging", "production"]
    },
    "regression_tests": {
      "path": "tests/regression/",
      "parallel_jobs": 4,
      "timeout": 1800,
      "critical": false,
      "schedule": "weekly",
      "environments": ["staging"]
    },
    "integration_tests": {
      "path": "tests/integration/",
      "parallel_jobs": 3,
      "timeout": 1200,
      "critical": true,
      "schedule": "daily",
      "environments": ["staging"]
    },
    "api_tests": {
      "path": "tests/api/",
      "parallel_jobs": 2,
      "timeout": 600,
      "critical": true,
      "schedule": "every_push",
      "environments": ["staging", "development"]
    },
    "performance_tests": {
      "path": "tests/performance/",
      "parallel_jobs": 1,
      "timeout": 3600,
      "critical": false,
      "schedule": "monthly",
      "environments": ["staging"]
    }
  },
  "optimization_settings": {
    "cache_dependencies": true,
    "reuse_volumes": true,
    "smart_retry": {
      "enabled": true,
      "max_attempts": 2,
      "only_flaky": true,
      "conditions": ["timeout", "connection_error", "external_service_unavailable"]
    },
    "resource_limits": {
      "cpu": "2",
      "memory": "4G",
      "concurrency": 4
    },
    "early_exit": {
      "enabled": true,
      "failure_threshold": 5,
      "stop_on_critical_failure": true
    },
    "incremental_testing": {
      "enabled": true,
      "based_on_changed_files": true,
      "fallback_to_full": false
    }
  }
}
```

---

**💡 Использование шаблонов:**

1. **GitLab CI**: Скопируйте `.gitlab-ci.yml` в корень проекта
2. **Docker**: Используйте `Dockerfile.test` и `docker-compose.test.yml` для контейнеризации
3. **Pytest**: Добавьте `pytest.ini` и `conftest.py` в проект
4. **Reporting**: Настройте `notification_config.json` под ваши нужды
5. **Scripts**: Используйте скрипты в CI pipeline
6. **Matrix**: Настройте `test_matrix.json` для оптимизации тестирования

**⚠️ Важно:** Адаптируйте шаблоны под специфику вашего проекта!