# Модуль 6: CI/CD и отчетность

## 🎯 Цели модуля (3 недели / 12 занятий)

**По окончании модуля студент сможет:**
- Настраивать CI/CD pipelines для автоматизированных тестов
- Генерировать профессиональные отчеты о тестировании
- Интегрировать тесты в GitLab CI, GitHub Actions и Jenkins
- Настройка мониторинга и алертинга тестов
- **Реализовывать тестирование в production-like средах**
- **Создавать dashboards для отслеживания качества**
- **Оптимизировать производительность тестов в CI**
- **Настраивать security и secrets management**
- **Реализовывать тестирование в разных средах (dev/staging/prod)**
- **Создавать метрики и KPI для тестирования**

## 👨‍🏫 Методические материалы для преподавателя

### Интеграция DevOps практик в тестирование:

**🎯 Особенности преподавания CI/CD:**
- **Практическая направленность:** Работа с реальными CI системами
- **Infrastructure as Code:** Понимание как кода инфраструктуры
- **Monitoring mindset:** Умение отслеживать и анализировать метрики
- **Troubleshooting skills:** Навыки диагностики проблем в CI
- **Security awareness:** Понимание безопасности CI/CD процессов
- **Production readiness:** Подготовка к работе в production средах
- **Metrics-driven approach:** Использование данных для принятия решений

### 🛠️ Инструменты DevOps для тестировщика

#### Расширенные инструменты мониторинга:
- **Grafana** - создание dashboards для метрик тестирования
- **Prometheus** - сбор и хранение метрик
- **ELK Stack** (Elasticsearch, Logstash, Kibana) - анализ логов
- **Datadog** - облачный monitoring
- **New Relic** - application performance monitoring

#### Security tools для CI/CD:
- **Snyk** - сканирование уязвимостей зависимостей
- **SonarQube** - static code analysis
- **OWASP ZAP** - security testing
- **HashiCorp Vault** - secrets management

#### Продвинутые команды CI/CD:
```bash
# Локальное тестирование GitLab CI
gitlab-runner exec docker test-job-name

# Локальное тестирование GitHub Actions
act -j test-job-name

# Мониторинг pipeline в реальном времени
watch -n 5 'curl -s "https://gitlab.example.com/api/v4/projects/123/pipelines"'

# Анализ performance тестов
python scripts/analyze_performance.py --input reports/ --output dashboard/

# Генерация security report
snyk test --json > security-report.json

# Backup и restore CI конфигураций
python scripts/backup_ci_config.py --project my-project --output backup/
```

**📋 Требуемые ресурсы:**
- Доступ к CI/CD платформам (GitLab, GitHub, Jenkins)
- Docker образы для тестирования
- Monitoring и logging инструменты
- Sample repositories с тестами
- **Готовые pipeline templates**
- **Test environments (dev/staging/prod access)**
- **Monitoring dashboards и alerting systems**
- **Security scanning tools**
- **Performance testing infrastructure**

### 📋 Подробный тайминг занятий модуля 6

#### Занятие 6.1: GitLab CI Pipeline fundamentals (90 минут)

**0-15 мин:** Введение в CI/CD концепции
- Что такое Continuous Integration и Delivery
- Преимущества автоматизации тестирования
- **Демонстрация реального pipeline**

**15-35 мин:** Теория - Архитектура GitLab CI
- Jobs, stages, и pipeline workflow
- Variables и secrets management
- Artifacts и caching механизм
- **Живая демонстрация pipeline структуры**

**35-60 мин:** Практика - Создание базового pipeline
- Настройка .gitlab-ci.yml файла
- Конфигурация test jobs
- Настройка artifact сохранения
- **Interactive coding session**

**60-80 мин:** Самостоятельная практика
- Студенты создают собственные pipelines
- Настройка разных stages
- **Индивидуальная помощь преподавателя**

**80-90 мин:** Закрепление материала
- Разбор типичных ошибок
- Ответы на вопросы
- Домашнее задание

#### Занятие 6.2: Расширенные возможности CI/CD (90 минут)

**0-20 мин:** Теория - Advanced CI/CD features
- Matrix builds и parallel execution
- Conditional job execution
- Trigger jobs и child pipelines
- **Сравнение подходов разных платформ**

**20-45 мин:** Практика - Complex pipeline scenarios
- Настройка multi-environment deployments
- Implementation of approval gates
- Integration with external services
- **Live demonstration**

**45-70 мин:** Практика - Monitoring и alerting
- Настройка Slack/GitLab notifications
- Creation of custom metrics
- Implementation of failure analysis
- **Hands-on configuration**

**70-85 мин:** Самостоятельная работа
- Students configure monitoring for their pipelines
- Setup alerting rules
- **Personal consultations**

**85-90 мин:** Завершение занятия
- Review of accomplished work
- Homework assignment

#### Занятие 6.3: Reporting и dashboard creation (90 минут)

**0-25 мин:** Теория - Allure и профессиональные отчеты
- Allure framework capabilities
- Custom reporters development
- Integration with CI systems
- **Showcase of professional reports**

**25-50 мин:** Практика - Dashboard creation
- Grafana dashboard setup
- Custom metrics visualization
- Real-time monitoring panels
- **Interactive dashboard building**

**50-75 мин:** Самостоятельная практика
- Создание собственных dashboards
- Настройка метрик и алертов
- **Individual support**

**75-90 мин:** Подведение итогов модуля
- Review of all CI/CD concepts
- Final Q&A session
- Course completion certificate
- **Next steps recommendations**

**⏰ Структура занятий по CI/CD:**
- 15 мин: Теория и best practices
- 30 мин: Live configuration demos
- 30 мин: Hands-on pipeline setup
- 15 мин: Troubleshooting и debugging

## ⚙️ Настройка CI/CD Pipelines

### GitLab CI Pipeline для автоматизации тестов

```yaml
# .gitlab-ci.yml - ПОЛНЫЙ PIPELINE ДЛЯ ТЕСТИРОВАНИЯ

stages:
  - setup
  - test
  - report
  - deploy

variables:
  # Конфигурационные переменные
  PYTHON_VERSION: "3.11"
  PLAYWRIGHT_BROWSERS_PATH: "$CI_PROJECT_DIR/ms-playwright"
  REPORTS_DIR: "$CI_PROJECT_DIR/reports"
  
  # Environment variables
  TEST_ENVIRONMENT: "staging"
  BASE_URL: "https://staging.example.com"

# SETUP STAGE
install_dependencies:
  stage: setup
  image: python:$PYTHON_VERSION
  before_script:
    - apt-get update && apt-get install -y curl jq
    - pip install --upgrade pip
  script:
    - pip install -r requirements.txt
    - playwright install --with-deps chromium firefox webkit
    - python -m pytest --collect-only tests/  # Проверка что тесты собираются
  artifacts:
    paths:
      - .venv/
      - ms-playwright/
    expire_in: 1 hour
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip/
      - ms-playwright/

# UNIT TESTS STAGE
unit_tests:
  stage: test
  image: python:$PYTHON_VERSION
  services:
    - postgres:13
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_pass
  script:
    - source .venv/bin/activate  # Если используется virtual environment
    - pytest tests/unit/ --junitxml=reports/unit-tests.xml --cov=src --cov-report=xml:reports/coverage.xml
  artifacts:
    reports:
      junit: reports/unit-tests.xml
      coverage_report:
        coverage_format: cobertura
        path: reports/coverage.xml
    paths:
      - reports/
    expire_in: 1 week
  coverage: '/TOTAL.*\s+(\d+%)$/'
  allow_failure: false

# API TESTS STAGE
api_tests:
  stage: test
  image: python:$PYTHON_VERSION
  script:
    - pytest tests/api/ --junitxml=reports/api-tests.xml -v
  artifacts:
    reports:
      junit: reports/api-tests.xml
    paths:
      - reports/
    expire_in: 1 week
  allow_failure: false

# UI TESTS STAGE
ui_tests:
  stage: test
  image: mcr.microsoft.com/playwright/python:v1.40.0-focal
  before_script:
    - pip install -r requirements.txt
  parallel:
    matrix:
      - BROWSER: [chromium, firefox, webkit]
        DEVICE: [desktop, mobile]
  script:
    - |
      pytest tests/ui/ \
        --browser=$BROWSER \
        --device=$DEVICE \
        --junitxml=reports/ui-tests-$BROWSER-$DEVICE.xml \
        --video=retain-on-failure \
        --screenshot=only-on-failure \
        --tracing=retain-on-failure
  artifacts:
    reports:
      junit: reports/ui-tests-$BROWSER-$DEVICE.xml
    paths:
      - reports/videos/
      - reports/screenshots/
      - reports/traces/
    expire_in: 1 week
    when: always
  allow_failure: true  # UI тесты могут быть нестабильны

# PERFORMANCE TESTS STAGE
performance_tests:
  stage: test
  image: python:$PYTHON_VERSION
  script:
    - |
      pytest tests/performance/ \
        --junitxml=reports/performance-tests.xml \
        --html=reports/performance-report.html
  artifacts:
    reports:
      junit: reports/performance-tests.xml
    paths:
      - reports/performance-report.html
    expire_in: 1 month
  only:
    - schedules  # Запуск по расписанию
    - master     # Или только в master ветке

# REPORT GENERATION STAGE
generate_reports:
  stage: report
  image: python:$PYTHON_VERSION
  needs:
    - job: unit_tests
    - job: api_tests
    - job: ui_tests
    - job: performance_tests
  script:
    - pip install allure-pytest
    - |
      allure generate \
        reports/allure-results/ \
        -o reports/allure-report/ \
        --clean
  artifacts:
    paths:
      - reports/allure-report/
    expire_in: 1 month
  dependencies:
    - unit_tests
    - api_tests
    - ui_tests
    - performance_tests

# DASHBOARD AND METRICS
publish_metrics:
  stage: report
  image: python:$PYTHON_VERSION
  script:
    - |
      # Генерация метрик для dashboard
      python scripts/generate_metrics.py \
        --input-reports reports/ \
        --output-json reports/metrics.json
  artifacts:
    reports:
      metrics: reports/metrics.json
    paths:
      - reports/metrics.json
    expire_in: 1 year

# DEPLOYMENT STAGE (Conditional)
deploy_if_tests_pass:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - |
      if [ "$CI_PIPELINE_SOURCE" = "merge_request_event" ]; then
        echo "Deploying to staging environment..."
        docker build -t $CI_REGISTRY_IMAGE:staging-$CI_COMMIT_SHA .
        docker push $CI_REGISTRY_IMAGE:staging-$CI_COMMIT_SHA
      elif [ "$CI_COMMIT_BRANCH" = "master" ]; then
        echo "Deploying to production..."
        docker build -t $CI_REGISTRY_IMAGE:prod-$CI_COMMIT_TAG .
        docker push $CI_REGISTRY_IMAGE:prod-$CI_COMMIT_TAG
      fi
  only:
    - merge_requests
    - master@your-group/your-project
  when: on_success

# SCHEDULED JOBS
scheduled_regression:
  stage: test
  image: python:$PYTHON_VERSION
  script:
    - pytest tests/regression/ --junitxml=reports/regression-tests.xml
  artifacts:
    reports:
      junit: reports/regression-tests.xml
  only:
    - schedules

# TRIGGER JOBS
trigger_external_pipeline:
  stage: deploy
  trigger:
    include:
      - project: 'infrastructure/deployment'
        file: '.gitlab-ci.yml'
    strategy: depend
  only:
    - master
  when: on_success

# CUSTOM TEMPLATES SECTION
.custom_cache_template: &custom_cache_definition
  cache:
    key: "${CI_JOB_NAME}"
    paths:
      - .venv/
      - .npm/
      - node_modules/
    policy: pull-push

.custom_artifact_template: &custom_artifact_definition
  artifacts:
    paths:
      - reports/
    reports:
      junit: reports/test-results.xml
    expire_in: 1 week
    when: always

# ENVIRONMENT-SPECIFIC CONFIGURATIONS
.environment_variables_template: &environment_variables
  variables:
    DB_HOST: $DB_HOST
    DB_PORT: $DB_PORT
    DB_NAME: $DB_NAME
    DB_USER: $DB_USER
    DB_PASS: $DB_PASS
    API_BASE_URL: $API_BASE_URL
    WEB_BASE_URL: $WEB_BASE_URL

# ПОЛЕЗНЫЕ СКРИПТЫ ДЛЯ CI:

# scripts/wait_for_services.py
"""
Скрипт ожидания readiness сервисов
"""

import time
import requests
from typing import List

def wait_for_services(services: List[str], timeout: int = 300):
    """Ожидание готовности сервисов"""
    start_time = time.time()
    
    for service_url in services:
        while time.time() - start_time < timeout:
            try:
                response = requests.get(service_url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Service {service_url} is ready")
                    break
            except requests.RequestException:
                pass
            
            print(f"⏳ Waiting for {service_url}...")
            time.sleep(5)
        else:
            raise TimeoutError(f"Service {service_url} did not become ready within {timeout} seconds")

if __name__ == "__main__":
    import sys
    services = sys.argv[1:] if len(sys.argv) > 1 else ["http://localhost:8000/health"]
    wait_for_services(services)
```

### GitHub Actions Workflow

```yaml
# .github/workflows/test-automation.yml

name: Test Automation Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 1'  # Еженедельно по понедельникам

env:
  PYTHON_VERSION: '3.11'
  PLAYWRIGHT_BROWSERS_PATH: '${{ github.workspace }}/ms-playwright'

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: |
            ~/.cache/pip
            ${{ env.PLAYWRIGHT_BROWSERS_PATH }}
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          playwright install --with-deps
      
      - name: Validate test collection
        run: python -m pytest --collect-only tests/

  unit-tests:
    needs: setup
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      
      - name: Restore cache
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      
      - name: Run unit tests
        run: |
          pytest tests/unit/ \
            --junitxml=reports/unit-test-results.xml \
            --cov=src \
            --cov-report=xml:reports/coverage.xml \
            --cov-report=html:reports/coverage-html
          
      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: reports/unit-test-results.xml
          
      - name: Publish Coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./reports/coverage.xml
          flags: unittests
          name: codecov-umbrella

  ui-tests:
    needs: setup
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox, webkit]
        shard: [1/3, 2/3, 3/3]
    steps:
      - uses: actions/checkout@v4
      
      - name: Restore Playwright browsers
        uses: actions/cache@v3
        with:
          path: ${{ env.PLAYWRIGHT_BROWSERS_PATH }}
          key: playwright-browsers-${{ runner.os }}
      
      - name: Run UI tests
        run: |
          pytest tests/ui/ \
            --browser=${{ matrix.browser }} \
            --shard=${{ matrix.shard }} \
            --junitxml=reports/ui-test-results-${{ matrix.browser }}-${{ matrix.shard }}.xml \
            --video=retain-on-failure \
            --screenshot=only-on-failure \
            --tracing=retain-on-failure
          
      - name: Upload test artifacts
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: test-results-${{ matrix.browser }}-${{ matrix.shard }}
          path: |
            reports/videos/
            reports/screenshots/
            reports/traces/
          retention-days: 7

  generate-dashboard:
    needs: [unit-tests, ui-tests]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Download all test results
        uses: actions/download-artifact@v3
        with:
          path: downloaded-artifacts
      
      - name: Generate Allure Report
        run: |
          docker run --rm \
            -v "${PWD}/downloaded-artifacts:/results" \
            -v "${PWD}/reports/allure-report:/allure-report" \
            frankescobar/allure-docker-service:2.21.0 \
            allure generate /results/*/*/reports/*.xml -o /allure-report --clean
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./reports/allure-report
          destination_dir: test-reports/${{ github.sha }}

  notify-slack:
    needs: [unit-tests, ui-tests]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Send Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#test-notifications'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## 📊 Генерация отчетов и метрик

### Allure Framework для профессиональных отчетов

```python
# ПРОФЕССИОНАЛЬНЫЕ ОТЧЕТЫ С ALLURE

class AllureReporting:
    def __init__(self):
        self.report_templates = {}
        self.metrics_collectors = {}
    
    def allure_decorators_examples(self):
        """Примеры декораторов Allure"""
        
        import allure
        import pytest
        
        @allure.feature("User Management")
        @allure.story("User Registration")
        @allure.severity(allure.severity_level.CRITICAL)
        @pytest.mark.parametrize("user_type", ["regular", "premium", "admin"])
        def test_user_registration(page, user_type):
            """Тест регистрации пользователя с Allure аннотациями"""
            
            with allure.step("Navigate to registration page"):
                page.goto("/register")
                allure.attach(
                    page.screenshot(),
                    name="Registration page",
                    attachment_type=allure.attachment_type.PNG
                )
            
            with allure.step(f"Fill registration form for {user_type} user"):
                page.fill("#email", f"{user_type}@test.com")
                page.fill("#password", "securePassword123")
                
                if user_type == "premium":
                    page.check("#premium-plan")
                
                allure.attach(
                    page.content(),
                    name="Form filled",
                    attachment_type=allure.attachment_type.HTML
                )
            
            with allure.step("Submit registration form"):
                with page.expect_response("**/api/register") as response_info:
                    page.click("#register-btn")
                
                response = response_info.value
                allure.attach(
                    str(response.status),
                    name="API Response Status",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            with allure.step("Verify successful registration"):
                expect(page).to_have_url("/dashboard")
                welcome_message = page.locator(".welcome-message")
                expect(welcome_message).to_be_visible()
                
                allure.attach(
                    welcome_message.text_content(),
                    name="Welcome message",
                    attachment_type=allure.attachment_type.TEXT
                )
    
    def custom_allure_attachments(self, page):
        """Пользовательские вложения Allure"""
        
        import allure
        import json
        from datetime import datetime
        
        def attach_test_metadata(test_name, browser_info, test_data):
            """Прикрепление метаданных теста"""
            
            # Информация о браузере
            allure.attach(
                json.dumps(browser_info, indent=2),
                name="Browser Information",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Тестовые данные
            allure.attach(
                json.dumps(test_data, indent=2),
                name="Test Data",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Скриншот с timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name=f"Screenshoot at {timestamp}",
                attachment_type=allure.attachment_type.PNG
            )
        
        def attach_network_logs(page):
            """Прикрепление network логов"""
            
            # Сбор network информации
            network_info = page.evaluate("""() => {
                return performance.getEntriesByType('navigation')[0];
            }""")
            
            allure.attach(
                json.dumps(network_info, indent=2, default=str),
                name="Network Performance Metrics",
                attachment_type=allure.attachment_type.JSON
            )
        
        def attach_console_logs(page):
            """Прикрепление console логов"""
            
            logs = []
            page.on("console", lambda msg: logs.append({
                "type": msg.type,
                "text": msg.text,
                "location": msg.location
            }))
            
            # В конце теста прикрепляем логи
            def attach_logs():
                allure.attach(
                    json.dumps(logs, indent=2),
                    name="Browser Console Logs",
                    attachment_type=allure.attachment_type.JSON
                )
            
            return attach_logs
    
    def allure_labels_and_links(self):
        """Allure labels и ссылки"""
        
        import allure
        
        @allure.label("layer", "UI")
        @allure.label("owner", "qa-team")
        @allure.link("https://jira.example.com/browse/PROJ-123", name="JIRA Issue")
        @allure.issue("BUG-456", "Known issue with login")
        @allure.testcase("TC-789", "Test case specification")
        def test_with_labels_and_links(page):
            """Тест с полной аннотацией Allure"""
            pass

# ГЕНЕРАЦИЯ МЕТРИК И DASHBOARDS:

class MetricsAndDashboards:
    def __init__(self):
        self.metrics_collector = {}
        self.dashboard_generator = {}
    
    def test_metrics_collector(self):
        """Сбор метрик тестирования"""
        
        import json
        from datetime import datetime
        from collections import defaultdict
        
        class TestMetricsCollector:
            def __init__(self):
                self.metrics = defaultdict(list)
                self.start_time = datetime.now()
            
            def collect_test_result(self, test_name, status, duration, metadata=None):
                """Сбор результата отдельного теста"""
                
                metric_entry = {
                    "test_name": test_name,
                    "status": status,
                    "duration_ms": duration * 1000,  # Преобразование в миллисекунды
                    "timestamp": datetime.now().isoformat(),
                    "metadata": metadata or {}
                }
                
                self.metrics[test_name].append(metric_entry)
            
            def collect_performance_metrics(self, page, test_name):
                """Сбор performance метрик"""
                
                perf_metrics = page.evaluate("""() => {
                    const nav = performance.getEntriesByType('navigation')[0];
                    const paint = performance.getEntriesByType('paint');
                    
                    return {
                        pageLoadTime: nav.loadEventEnd - nav.fetchStart,
                        domContentLoaded: nav.domContentLoadedEventEnd - nav.fetchStart,
                        firstPaint: paint.find(p => p.name === 'first-paint')?.startTime,
                        firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime
                    };
                }""")
                
                self.metrics[f"{test_name}_perf"].append({
                    "timestamp": datetime.now().isoformat(),
                    "metrics": perf_metrics
                })
            
            def generate_summary_report(self):
                """Генерация сводного отчета"""
                
                summary = {
                    "report_generated": datetime.now().isoformat(),
                    "total_tests": sum(len(results) for results in self.metrics.values()),
                    "passed_tests": sum(1 for results in self.metrics.values() 
                                      for result in results if result["status"] == "passed"),
                    "failed_tests": sum(1 for results in self.metrics.values() 
                                      for result in results if result["status"] == "failed"),
                    "average_duration": self._calculate_average_duration(),
                    "slowest_tests": self._get_slowest_tests(limit=10),
                    "flaky_tests": self._identify_flaky_tests()
                }
                
                return summary
            
            def _calculate_average_duration(self):
                """Расчет средней продолжительности тестов"""
                all_durations = [
                    result["duration_ms"] 
                    for results in self.metrics.values() 
                    for result in results 
                    if "duration_ms" in result
                ]
                return sum(all_durations) / len(all_durations) if all_durations else 0
            
            def _get_slowest_tests(self, limit=10):
                """Получение самых медленных тестов"""
                test_averages = []
                
                for test_name, results in self.metrics.items():
                    durations = [r["duration_ms"] for r in results if "duration_ms" in r]
                    if durations:
                        avg_duration = sum(durations) / len(durations)
                        test_averages.append((test_name, avg_duration))
                
                return sorted(test_averages, key=lambda x: x[1], reverse=True)[:limit]
            
            def _identify_flaky_tests(self, threshold=0.3):
                """Идентификация flaky тестов"""
                flaky_tests = []
                
                for test_name, results in self.metrics.items():
                    if len(results) < 3:  # Нужно минимум 3 запуска
                        continue
                    
                    statuses = [r["status"] for r in results]
                    pass_rate = statuses.count("passed") / len(statuses)
                    
                    if 0.3 <= pass_rate <= 0.7:  # Сильно колеблющийся pass rate
                        flaky_tests.append({
                            "test_name": test_name,
                            "pass_rate": pass_rate,
                            "total_runs": len(results),
                            "recent_status": statuses[-5:]  # Последние 5 запусков
                        })
                
                return flaky_tests
        
        return TestMetricsCollector()
    
    def dashboard_generation(self):
        """Генерация dashboard для мониторинга"""
        
        def generate_html_dashboard(metrics_data, output_file="dashboard.html"):
            """Генерация HTML dashboard"""
            
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Test Automation Dashboard</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .metric-card { 
                        border: 1px solid #ddd; 
                        padding: 15px; 
                        margin: 10px; 
                        border-radius: 5px;
                        display: inline-block;
                        min-width: 200px;
                    }
                    .passed { background-color: #d4edda; border-color: #c3e6cb; }
                    .failed { background-color: #f8d7da; border-color: #f5c6cb; }
                    .chart-container { width: 600px; height: 400px; margin: 20px; }
                </style>
            </head>
            <body>
                <h1>Test Automation Dashboard</h1>
                
                <div class="metric-card passed">
                    <h3>Passed Tests</h3>
                    <h2>{passed_count}</h2>
                </div>
                
                <div class="metric-card failed">
                    <h3>Failed Tests</h3>
                    <h2>{failed_count}</h2>
                </div>
                
                <div class="metric-card">
                    <h3>Pass Rate</h3>
                    <h2>{pass_rate:.1f}%</h2>
                </div>
                
                <div class="metric-card">
                    <h3>Average Duration</h3>
                    <h2>{avg_duration:.2f}s</h2>
                </div>
                
                <div class="chart-container">
                    <canvas id="durationChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <canvas id="statusChart"></canvas>
                </div>
                
                <script>
                    // Duration chart
                    new Chart(document.getElementById('durationChart'), {{
                        type: 'bar',
                        data: {{
                            labels: {slowest_test_names},
                            datasets: [{{
                                label: 'Average Duration (seconds)',
                                data: {slowest_test_durations},
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderWidth: 1
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            scales: {{
                                y: {{
                                    beginAtZero: true
                                }}
                            }}
                        }}
                    }});
                    
                    // Status chart
                    new Chart(document.getElementById('statusChart'), {{
                        type: 'doughnut',
                        data: {{
                            labels: ['Passed', 'Failed'],
                            datasets: [{{
                                data: [{passed_count}, {failed_count}],
                                backgroundColor: ['#4CAF50', '#F44336']
                            }}]
                        }},
                        options: {{
                            responsive: true
                        }}
                    }});
                </script>
            </body>
            </html>
            """
            
            # Подстановка данных
            passed_count = metrics_data["passed_tests"]
            failed_count = metrics_data["failed_tests"]
            pass_rate = (passed_count / (passed_count + failed_count)) * 100 if (passed_count + failed_count) > 0 else 0
            avg_duration = metrics_data["average_duration"] / 1000  # В секундах
            
            # Данные для графиков
            slowest_tests = metrics_data["slowest_tests"][:5]
            slowest_test_names = json.dumps([test[0] for test in slowest_tests])
            slowest_test_durations = json.dumps([test[1]/1000 for test in slowest_tests])  # В секундах
            
            # Формирование HTML
            html_content = html_template.format(
                passed_count=passed_count,
                failed_count=failed_count,
                pass_rate=pass_rate,
                avg_duration=avg_duration,
                slowest_test_names=slowest_test_names,
                slowest_test_durations=slowest_test_durations
            )
            
            # Сохранение файла
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return output_file

# ИНТЕГРАЦИЯ С MONITORING СИСТЕМАМИ:

class MonitoringIntegration:
    def prometheus_metrics_export(self):
        """Экспорт метрик в Prometheus"""
        
        def generate_prometheus_metrics(metrics_data, output_file="metrics.prom"):
            """Генерация метрик в формате Prometheus"""
            
            prometheus_content = f"""
            # TYPE test_total counter
            # HELP test_total Total number of tests executed
            test_total {{status="passed"}} {metrics_data["passed_tests"]}
            test_total {{status="failed"}} {metrics_data["failed_tests"]}
            
            # TYPE test_duration_seconds gauge
            # HELP test_duration_seconds Average test duration in seconds
            test_duration_seconds {{type="average"}} {metrics_data["average_duration"] / 1000}
            
            # TYPE test_flaky_count gauge
            # HELP test_flaky_count Number of flaky tests identified
            test_flaky_count {len(metrics_data["flaky_tests"])}
            
            # TYPE test_slow_count gauge
            # HELP test_slow_count Number of tests slower than threshold
            test_slow_count {len([t for t in metrics_data["slowest_tests"] if t[1] > 10000])}
            """
            
            with open(output_file, 'w') as f:
                f.write(prometheus_content)
            
            return output_file
    
    def slack_notification_integration(self):
        """Интеграция с Slack notifications"""
        
        def send_slack_notification(webhook_url, metrics_data):
            """Отправка уведомления в Slack"""
            
            import requests
            import json
            
            # Определение цвета сообщения
            pass_rate = metrics_data["passed_tests"] / (metrics_data["passed_tests"] + metrics_data["failed_tests"])
            color = "good" if pass_rate >= 0.9 else "warning" if pass_rate >= 0.8 else "danger"
            
            # Формирование сообщения
            message = {
                "attachments": [{
                    "color": color,
                    "title": "Test Automation Results",
                    "fields": [
                        {
                            "title": "Total Tests",
                            "value": str(metrics_data["passed_tests"] + metrics_data["failed_tests"]),
                            "short": True
                        },
                        {
                            "title": "Passed",
                            "value": str(metrics_data["passed_tests"]),
                            "short": True
                        },
                        {
                            "title": "Failed",
                            "value": str(metrics_data["failed_tests"]),
                            "short": True
                        },
                        {
                            "title": "Pass Rate",
                            "value": f"{pass_rate*100:.1f}%",
                            "short": True
                        },
                        {
                            "title": "Average Duration",
                            "value": f"{metrics_data['average_duration']/1000:.2f}s",
                            "short": True
                        }
                    ],
                    "footer": "Test Automation Pipeline",
                    "ts": int(datetime.now().timestamp())
                }]
            }
            
            # Отправка запроса
            response = requests.post(webhook_url, json=message)
            return response.status_code == 200

# ЛУЧШИЕ ПРАКТИКИ ОТЧЕТНОСТИ:
reporting_best_practices = [
    "Используйте Allure для rich reporting",
    "Собирайте performance метрики в реальном времени",
    "Интегрируйте отчеты в CI/CD pipeline",
    "Настройте автоматические уведомления",
    "Храните историю тестов для trend анализа",
    "Создавайте executive dashboards для менеджмента",
    "Экспортируйте метрики в monitoring системы"
]
```

## 🚀 Оптимизация производительности

### Ускорение тестов в CI/CD

```python
# ОПТИМИЗАЦИЯ ПРОИЗВОДИТЕЛЬНОСТИ ТЕСТОВ

class TestPerformanceOptimization:
    def __init__(self):
        self.optimization_strategies = {}
        self.parallelization_techniques = {}
    
    def test_parallelization(self):
        """Параллельное выполнение тестов"""
        
        # pytest.ini для параллельного выполнения
        pytest_ini_content = """
        [tool:pytest]
        addopts = -n auto --dist worksteal
        markers =
            serial: mark test to run serially
            slow: mark test as slow
            fast: mark test as fast
        """
        
        # Конфигурация xdist для оптимального распределения
        def optimize_xdist_configuration():
            return {
                "processes": "auto",  # Автоматическое определение количества процессов
                "distribution": "worksteal",  # Эффективное распределение нагрузки
                "max_worker_restart": 3,  # Максимальное количество перезапусков worker'ов
                "rsyncdirs": ["src/", "tests/", "config/"],  # Директории для синхронизации
                "rsyncignore": ["*.pyc", "__pycache__", ".git"]  # Игнорируемые файлы
            }
    
    def test_sharding(self):
        """Sharding для распределения тестов"""
        
        def generate_shard_commands(total_shards=4):
            """Генерация команд для sharding"""
            
            shard_commands = []
            for shard_num in range(1, total_shards + 1):
                command = f"pytest --shard={shard_num}/{total_shards} tests/"
                shard_commands.append(command)
            
            return shard_commands
        
        # Пример использования в CI:
        ci_sharding_example = """
        # GitLab CI matrix для sharding
        test_shards:
          stage: test
          parallel:
            matrix:
              - SHARD: [1/4, 2/4, 3/4, 4/4]
          script:
            - pytest --shard=$SHARD tests/ --junitxml=reports/results-$SHARD.xml
        """
        
        return ci_sharding_example
    
    def selective_test_execution(self):
        """Селективное выполнение тестов"""
        
        def determine_affected_tests(changed_files):
            """Определение тестов, которые нужно запустить"""
            
            test_mapping = {
                "src/user/": ["tests/unit/test_user.py", "tests/api/test_user_api.py"],
                "src/payment/": ["tests/unit/test_payment.py", "tests/integration/test_payment_flow.py"],
                "src/ui/": ["tests/ui/"],
                "requirements.txt": ["tests/"]  # Все тесты при изменении зависимостей
            }
            
            affected_tests = set()
            
            for changed_file in changed_files:
                for source_path, test_files in test_mapping.items():
                    if changed_file.startswith(source_path):
                        affected_tests.update(test_files)
            
            return list(affected_tests)
        
        def git_based_test_selection():
            """Выбор тестов на основе изменений в Git"""
            
            import subprocess
            
            def get_changed_files(base_branch="origin/main"):
                """Получение списка измененных файлов"""
                result = subprocess.run([
                    "git", "diff", "--name-only", base_branch
                ], capture_output=True, text=True)
                
                return result.stdout.strip().split('\n')
            
            def select_tests_for_changes():
                """Выбор тестов для запуска"""
                changed_files = get_changed_files()
                affected_tests = determine_affected_tests(changed_files)
                
                if not affected_tests:
                    return ["tests/smoke/"]  # Smoke тесты по умолчанию
                
                return affected_tests
    
    def caching_strategies(self):
        """Стратегии кэширования для ускорения"""
        
        caching_configurations = {
            "pip_cache": {
                "paths": ["~/.cache/pip/", ".pip-cache/"],
                "key_template": "${CI_JOB_NAME}-${CI_COMMIT_REF_SLUG}-${CACHE_VERSION}"
            },
            
            "playwright_cache": {
                "paths": ["ms-playwright/", "~/.cache/ms-playwright/"],
                "key_template": "playwright-browsers-${OS}-${PLAYWRIGHT_VERSION}"
            },
            
            "docker_cache": {
                "paths": [".docker-cache/"],
                "key_template": "docker-layers-${CI_COMMIT_SHA}"
            },
            
            "test_results_cache": {
                "paths": ["reports/.cache/"],
                "key_template": "test-results-${TEST_SUITE_HASH}"
            }
        }
        
        return caching_configurations
    
    def resource_optimization(self):
        """Оптимизация использования ресурсов"""
        
        def optimize_docker_images():
            """Оптимизация Docker образов для тестов"""
            
            optimized_dockerfile = """
            # Multi-stage build для минимизации размера
            FROM python:3.11-slim as base
            RUN apt-get update && apt-get install -y \\
                curl \\
                jq \\
                && rm -rf /var/lib/apt/lists/*
            
            FROM base as builder
            COPY requirements.txt .
            RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt
            
            FROM base
            COPY --from=builder /wheels /wheels
            RUN pip install --no-cache /wheels/*
            
            # Только необходимые зависимости для Playwright
            RUN playwright install chromium
            """
            
            return optimized_dockerfile
        
        def resource_limits_configuration():
            """Конфигурация лимитов ресурсов"""
            
            return {
                "memory_limit": "4G",      # Лимит памяти
                "cpu_limit": "2",          # Лимит CPU
                "timeout": "30m",          # Таймаут выполнения
                "parallel_jobs": 4,        # Параллельные jobs
                "retry_attempts": 2        # Попытки повтора
            }

# МОНИТОРИНГ ПРОИЗВОДИТЕЛЬНОСТИ:
performance_monitoring = [
    "Отслеживайте время выполнения каждого теста",
    "Мониторьте использование памяти и CPU",
    "Анализируйте тренды производительности",
    "Идентифицируйте и устраняйте bottleneck'и",
    "Оптимизируйте самые медленные тесты",
    "Используйте profiling для глубокого анализа",
    "Настройте alerting для degradation производительности"
]
```

## ❓ Ответы на вопросы студентов

### CI/CD и инфраструктурные вопросы

**Q: Как обрабатывать secrets в CI/CD pipeline?**

A:
```python
# БЕЗОПАСНАЯ РАБОТА С SECRETS

class SecureSecretsManagement:
    def __init__(self):
        self.secret_handling_patterns = {}
    
    def environment_variables_approach(self):
        """Работа с secrets через environment variables"""
        
        # .env.example файл (без реальных значений)
        env_example = """
        # Database Configuration
        DB_HOST=localhost
        DB_PORT=5432
        DB_NAME=test_db
        DB_USER=db_user
        DB_PASS=your_password_here
        
        # API Keys
        API_KEY=your_api_key_here
        SECRET_KEY=your_secret_key_here
        
        # External Services
        SMTP_HOST=smtp.example.com
        SMTP_USER=email_user
        SMTP_PASS=email_password
        """
        
        # CI/CD конфигурация secrets
        gitlab_ci_secrets = """
        variables:
          DB_HOST: $DATABASE_HOST
          DB_PORT: $DATABASE_PORT
          DB_NAME: $DATABASE_NAME
          DB_USER: $DATABASE_USER
          DB_PASS: $DATABASE_PASSWORD
          API_KEY: $EXTERNAL_API_KEY
          SECRET_KEY: $APPLICATION_SECRET_KEY
        """
        
        # Python код для безопасной работы с secrets
        def secure_secret_access():
            import os
            from typing import Optional
            
            class SecretManager:
                def __init__(self):
                    self._secrets_cache = {}
                
                def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
                    """Безопасное получение secret"""
                    if key in self._secrets_cache:
                        return self._secrets_cache[key]
                    
                    value = os.getenv(key, default)
                    if value and value != default:
                        # Маскирование для логов
                        self._secrets_cache[key] = value
                        return value
                    return None
                
                def get_required_secret(self, key: str) -> str:
                    """Получение обязательного secret"""
                    value = self.get_secret(key)
                    if not value:
                        raise ValueError(f"Required secret {key} is not set")
                    return value
            
            return SecretManager()
    
    def vault_integration(self):
        """Интеграция с HashiCorp Vault"""
        
        def vault_secret_retrieval():
            """Получение secrets из Vault"""
            
            import hvac
            
            class VaultClient:
                def __init__(self, vault_url: str, role_id: str, secret_id: str):
                    self.client = hvac.Client(url=vault_url)
                    self.authenticate(role_id, secret_id)
                
                def authenticate(self, role_id: str, secret_id: str):
                    """AppRole аутентификация"""
                    self.client.auth.approle.login(
                        role_id=role_id,
                        secret_id=secret_id
                    )
                
                def get_secret(self, path: str, key: str) -> str:
                    """Получение secret из Vault"""
                    secret_response = self.client.secrets.kv.v2.read_secret_version(
                        path=path
                    )
                    return secret_response['data']['data'][key]
            
            # Использование в CI/CD
            def ci_secret_injection(vault_client):
                """Инъекция secrets в CI environment"""
                secrets = {
                    'DB_PASSWORD': vault_client.get_secret('database', 'password'),
                    'API_KEY': vault_client.get_secret('external-services', 'api_key'),
                    'ENCRYPTION_KEY': vault_client.get_secret('app-config', 'encryption_key')
                }
                
                # Установка в environment variables
                for key, value in secrets.items():
                    os.environ[key] = value
                
                return secrets
    
    def kubernetes_secrets(self):
        """Работа с Kubernetes secrets"""
        
        def k8s_secret_mounting():
            """Монтирование secrets в Kubernetes pods"""
            
            k8s_pod_config = """
            apiVersion: v1
            kind: Pod
            metadata:
              name: test-runner
            spec:
              containers:
              - name: test-container
                image: test-image:latest
                envFrom:
                - secretRef:
                    name: test-secrets
                volumeMounts:
                - name: secret-volume
                  mountPath: /etc/secrets
                  readOnly: true
              volumes:
              - name: secret-volume
                secret:
                  secretName: test-certificates
            """
            
            return k8s_pod_config

# ЛУЧШИЕ ПРАКТИКИ ДЛЯ SECRETS:
secrets_best_practices = [
    "Никогда не коммитьте настоящие secrets в репозиторий",
    "Используйте secrets management системы (Vault, AWS Secrets Manager)",
    "Ротируйте secrets регулярно",
    "Ограничивайте доступ к secrets по принципу least privilege",
    "Маскируйте secrets в логах и отчетах",
    "Используйте разные secrets для разных environments",
    "Регулярно аудируйте доступ к secrets"
]
```

## 📋 Подробный тайминг занятий

### Занятие 6.1: Введение в CI/CD для тестирования (90 минут)

**0-15 мин: Теория CI/CD для тестов**
- Основные концепции CI/CD
- Преимущества автоматизации тестов в pipeline
- Архитектура тестовых pipeline
- **Демонстрация реального pipeline**

**15-40 мин: Практика - Настройка GitLab CI**
- Создание .gitlab-ci.yml файла
- Настройка stages и jobs
- Конфигурация artifacts и caching
- **Live coding pipeline конфигурации**

**40-65 мин: Hands-on практика**
- Студенты создают свои pipeline
- Настройка параллельного выполнения
- Интеграция с тестовыми фреймворками
- **Индивидуальная помощь преподавателя**

**65-80 мин: Troubleshooting и debugging**
- Типичные проблемы в CI/CD
- Методы диагностики pipeline issues
- Оптимизация времени выполнения
- **Разбор реальных case studies**

**80-90 мин: Закрепление и домашнее задание**
- Обзор пройденного материала
- Ответы на вопросы
- Назначение домашнего задания
- **Анонс следующего занятия**

---
*Модуль 6 готовит студентов к production-ready автоматизации тестирования*