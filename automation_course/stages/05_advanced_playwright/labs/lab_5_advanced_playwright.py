# 🧪 Лабораторная работа 5: Расширенные возможности Playwright

## Цель работы
Освоить продвинутые техники автоматизации тестирования с использованием Playwright, включая параллельное выполнение, визуальное тестирование и интеграцию с CI/CD.

## Оборудование и ПО
- Python 3.8+
- Playwright с расширенными возможностями
- pytest-playwright
- Allure для отчетности
- Docker (для CI/CD)

## Теоретическая часть

### Расширенные возможности Playwright:

🧪 **Параллельное тестирование** - одновременный запуск множества тестов
🎭 **Визуальное тестирование** - сравнение скриншотов для обнаружения изменений UI
🔄 **Retry механизм** - автоматический перезапуск упавших тестов
📊 **Расширенная отчетность** - детальные отчеты с артефактами
🌐 **Network interception** - контроль и модификация сетевых запросов
📱 **Device emulation** - тестирование под различные устройства и ориентации

## Практические задания

### Задание 1: Параллельное тестирование (25 баллов)

Создайте файл `test_parallel_execution.py`:

```python
import pytest
import asyncio
from playwright.async_api import async_playwright
from concurrent.futures import ThreadPoolExecutor
import time

class ParallelTestRunner:
    """Класс для параллельного выполнения тестов"""
    
    def __init__(self, max_workers=3):
        self.max_workers = max_workers
        self.results = []
    
    async def run_single_test(self, test_config):
        """Выполнить один тест"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                start_time = time.time()
                await page.goto(test_config["url"])
                
                # Выполняем специфичные действия для этого теста
                if test_config["type"] == "search":
                    await page.fill("#search-box", test_config["query"])
                    await page.click("#search-button")
                    await page.wait_for_selector(".search-results")
                    
                elif test_config["type"] == "form":
                    await page.fill("#name", test_config["name"])
                    await page.fill("#email", test_config["email"])
                    await page.click("#submit-form")
                    await page.wait_for_selector(".success-message")
                
                execution_time = time.time() - start_time
                
                return {
                    "test_name": test_config["name"],
                    "status": "PASSED",
                    "execution_time": execution_time,
                    "url": test_config["url"]
                }
                
            except Exception as e:
                return {
                    "test_name": test_config["name"],
                    "status": "FAILED",
                    "error": str(e),
                    "url": test_config["url"]
                }
            finally:
                await browser.close()

def test_concurrent_search_scenarios():
    """Тест параллельного выполнения поисковых сценариев"""
    
    test_configs = [
        {
            "name": "Search Test 1",
            "url": "https://testpages.eviltester.com/styled/basic-html-form-test.html",
            "type": "form",
            "name": "John Doe",
            "email": "john@example.com"
        },
        {
            "name": "Search Test 2", 
            "url": "https://testpages.eviltester.com/styled/find-by-playground-test.html",
            "type": "search",
            "query": "Playground"
        },
        {
            "name": "Search Test 3",
            "url": "https://httpbin.org/forms/post",
            "type": "form", 
            "name": "Jane Smith",
            "email": "jane@example.com"
        }
    ]
    
    runner = ParallelTestRunner(max_workers=3)
    
    # Выполняем тесты параллельно
    async def run_all_tests():
        tasks = [runner.run_single_test(config) for config in test_configs]
        results = await asyncio.gather(*tasks)
        return results
    
    # Запуск асинхронного выполнения
    results = asyncio.run(run_all_tests())
    
    # Анализ результатов
    passed_tests = [r for r in results if r["status"] == "PASSED"]
    failed_tests = [r for r in results if r["status"] == "FAILED"]
    
    print(f"Результаты параллельного выполнения:")
    print(f"Успешно: {len(passed_tests)}")
    print(f"Провалено: {len(failed_tests)}")
    
    for result in results:
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"{status_icon} {result['test_name']} - {result['status']}")
        if "execution_time" in result:
            print(f"   Время выполнения: {result['execution_time']:.2f} сек")
    
    assert len(passed_tests) >= 2, "Минимум 2 теста должны пройти успешно"

def test_browser_isolation():
    """Тест изоляции браузеров при параллельном выполнении"""
    
    async def run_isolated_test(session_id):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            # Уникальные данные для каждой сессии
            test_data = f"User_{session_id}_{int(time.time())}"
            
            await page.goto("https://httpbin.org/post")
            await page.fill("#custname", test_data)
            await page.click("form button")
            
            # Проверяем, что данные уникальны
            content = await page.text_content("pre")
            assert test_data in content, f"Данные сессии {session_id} не найдены"
            
            await browser.close()
            return f"Session {session_id} completed"
    
    # Запускаем 5 изолированных сессий параллельно
    async def run_multiple_sessions():
        tasks = [run_isolated_test(i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        return results
    
    results = asyncio.run(run_multiple_sessions())
    assert len(results) == 5, "Все сессии должны завершиться успешно"
    print("✅ Все изолированные сессии завершены успешно")
```

### Задание 2: Визуальное тестирование (20 баллов)

Создайте файл `test_visual_regression.py`:

```python
import pytest
from playwright.sync_api import sync_playwright
import hashlib
import os
from PIL import Image, ImageChops
import numpy as np

class VisualTester:
    """Класс для визуального тестирования"""
    
    def __init__(self, baseline_dir="baselines", current_dir="current", diff_dir="diffs"):
        self.baseline_dir = baseline_dir
        self.current_dir = current_dir
        self.diff_dir = diff_dir
        self._create_directories()
    
    def _create_directories(self):
        """Создать необходимые директории"""
        for directory in [self.baseline_dir, self.current_dir, self.diff_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def get_image_hash(self, image_path):
        """Получить хеш изображения"""
        with open(image_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def compare_images(self, baseline_path, current_path, threshold=5):
        """Сравнить два изображения"""
        baseline = Image.open(baseline_path)
        current = Image.open(current_path)
        
        # Проверка размеров
        if baseline.size != current.size:
            return False, "Different sizes"
        
        # Сравнение пикселей
        diff = ImageChops.difference(baseline, current)
        diff_array = np.array(diff)
        
        # Подсчет отличающихся пикселей
        diff_percentage = (np.count_nonzero(diff_array) / diff_array.size) * 100
        
        return diff_percentage <= threshold, f"Difference: {diff_percentage:.2f}%"
    
    def save_baseline(self, page, test_name):
        """Сохранить baseline скриншот"""
        baseline_path = os.path.join(self.baseline_dir, f"{test_name}.png")
        page.screenshot(path=baseline_path, full_page=True)
        return baseline_path
    
    def compare_with_baseline(self, page, test_name):
        """Сравнить текущий скриншот с baseline"""
        current_path = os.path.join(self.current_dir, f"{test_name}.png")
        baseline_path = os.path.join(self.baseline_dir, f"{test_name}.png")
        diff_path = os.path.join(self.diff_dir, f"{test_name}_diff.png")
        
        # Создаем текущий скриншот
        page.screenshot(path=current_path, full_page=True)
        
        # Если baseline не существует, создаем его
        if not os.path.exists(baseline_path):
            self.save_baseline(page, test_name)
            return True, "Baseline created"
        
        # Сравниваем изображения
        is_similar, message = self.compare_images(baseline_path, current_path)
        
        # Если есть различия, сохраняем diff
        if not is_similar:
            baseline_img = Image.open(baseline_path)
            current_img = Image.open(current_path)
            diff = ImageChops.difference(baseline_img, current_img)
            diff.save(diff_path)
        
        return is_similar, message

def test_homepage_visual_consistency():
    """Тест визуальной консистентности главной страницы"""
    
    visual_tester = VisualTester()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            page.goto("https://testpages.eviltester.com/styled/index.html")
            page.wait_for_load_state("networkidle")
            
            # Сравнение с baseline
            is_same, message = visual_tester.compare_with_baseline(page, "homepage")
            
            if not is_same:
                print(f"⚠️  Визуальные изменения обнаружены: {message}")
                print(f"📸 Diff сохранен в: {visual_tester.diff_dir}")
            else:
                print("✅ Визуальная консистентность подтверждена")
            
            assert is_same, f"Визуальные изменения: {message}"
            
        finally:
            browser.close()

@pytest.mark.parametrize("viewport_size", [
    {"width": 1920, "height": 1080},  # Desktop
    {"width": 1024, "height": 768},   # Tablet
    {"width": 375, "height": 667},    # Mobile
])
def test_responsive_design(viewport_size):
    """Тест адаптивного дизайна на разных устройствах"""
    
    visual_tester = VisualTester()
    device_name = f"{viewport_size['width']}x{viewport_size['height']}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport=viewport_size)
        
        try:
            page.goto("https://testpages.eviltester.com/styled/index.html")
            page.wait_for_load_state("networkidle")
            
            test_name = f"responsive_homepage_{device_name}"
            is_same, message = visual_tester.compare_with_baseline(page, test_name)
            
            print(f"📱 {device_name}: {'✅ Совпадает' if is_same else '❌ Различия'}")
            
        finally:
            browser.close()

def test_component_visual_testing():
    """Тест визуального отображения компонентов"""
    
    visual_tester = VisualTester()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Тестируем различные компоненты
            components = [
                ("buttons", "https://testpages.eviltester.com/styled/buttons-test.html"),
                ("forms", "https://testpages.eviltester.com/styled/basic-html-form-test.html"),
                ("tables", "https://testpages.eviltester.com/styled/tag/table.html")
            ]
            
            for component_name, url in components:
                page.goto(url)
                page.wait_for_load_state("networkidle")
                
                # Тестируем каждый компонент отдельно
                component_locator = page.locator(f".{component_name}-section, #{component_name}, [data-component='{component_name}']")
                if component_locator.count() > 0:
                    component_locator.first.screenshot(
                        path=f"{visual_tester.current_dir}/{component_name}_component.png"
                    )
                else:
                    # Если нет специфичного локатора, скриншот всей страницы
                    page.screenshot(path=f"{visual_tester.current_dir}/{component_name}_page.png")
                
                print(f"📸 Скриншот компонента '{component_name}' сохранен")
                
        finally:
            browser.close()
```

### Задание 3: Network Interception и Mocking (20 баллов)

Создайте файл `test_network_interception.py`:

```python
import pytest
from playwright.sync_api import sync_playwright, Route, Request
import json

def test_api_mocking():
    """Тест мокирования API ответов"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Мокируем API вызовы
        def handle_user_api(route: Route, request: Request):
            # Мокируем ответ для получения пользователя
            mock_response = {
                "id": 123,
                "name": "Mocked User",
                "email": "mocked@example.com",
                "status": "active"
            }
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(mock_response)
            )
        
        def handle_error_api(route: Route, request: Request):
            # Мокируем ошибку
            route.fulfill(
                status=500,
                content_type="application/json",
                body=json.dumps({"error": "Internal Server Error"})
            )
        
        try:
            # Применяем маршруты
            page.route("**/api/users/123", handle_user_api)
            page.route("**/api/error-endpoint", handle_error_api)
            
            # Тестируем мокированные ответы
            page.goto("https://httpbin.org/get")  # Любой сайт для демонстрации
            
            # Выполняем запросы к замоканным эндпоинтам
            user_response = page.evaluate("""async () => {
                const response = await fetch('/api/users/123');
                return await response.json();
            }""")
            
            assert user_response["name"] == "Mocked User"
            assert user_response["id"] == 123
            
            print("✅ API мокирование работает корректно")
            
        finally:
            browser.close()

def test_network_throttling():
    """Тест ограничения скорости сети"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # Эмуляция медленной сети
        context.set_offline(False)
        page = context.new_page()
        
        try:
            # Эмуляция 3G сети
            page.emulate_network_conditions(
                offline=False,
                latency=100,      #_additional latency (ms)
                download_throughput=500 * 1024,  # 500 Kbps
                upload_throughput=500 * 1024     # 500 Kbps
            )
            
            start_time = page.evaluate("() => performance.now()")
            page.goto("https://testpages.eviltester.com/styled/index.html")
            end_time = page.evaluate("() => performance.now()")
            
            load_time = (end_time - start_time) / 1000  # в секундах
            print(f"⏱️  Время загрузки при 3G: {load_time:.2f} секунд")
            
            # Страница должна загрузиться дольше из-за ограничений
            assert load_time > 1.0, "Загрузка должна быть медленной при эмуляции 3G"
            
        finally:
            browser.close()

def test_request_blocking():
    """Тест блокировки определенных запросов"""
    
    blocked_requests = []
    allowed_requests = []
    
    def handle_request(route, request):
        url = request.url
        
        # Блокируем рекламу и трекеры
        if any(blocked in url for blocked in ['adservice', 'analytics', 'facebook', 'google-analytics']):
            blocked_requests.append(url)
            route.abort()
        else:
            allowed_requests.append(url)
            route.continue_()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Устанавливаем обработчик запросов
        page.route("**/*", handle_request)
        
        try:
            page.goto("https://testpages.eviltester.com/styled/index.html")
            
            print(f"🚫 Заблокировано запросов: {len(blocked_requests)}")
            print(f"✅ Разрешено запросов: {len(allowed_requests)}")
            
            # Проверяем, что основные ресурсы загрузились
            assert page.title() != "", "Страница должна загрузиться"
            
            if blocked_requests:
                print("Заблокированные запросы:")
                for req in blocked_requests[:5]:  # Показываем первые 5
                    print(f"  - {req}")
            
        finally:
            browser.close()

def test_authentication_interception():
    """Тест перехвата и модификации аутентификационных запросов"""
    
    auth_tokens = []
    
    def intercept_auth_request(route, request):
        # Перехватываем запросы на аутентификацию
        if "/login" in request.url or "/auth" in request.url:
            headers = {
                **request.headers,
                "Authorization": "Bearer mocked-jwt-token",
                "X-Custom-Auth": "intercepted"
            }
            route.continue_(headers=headers)
            auth_tokens.append("mocked-jwt-token")
        else:
            route.continue_()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.route("**/*", intercept_auth_request)
        
        try:
            page.goto("https://httpbin.org/headers")
            
            # Проверяем, что заголовки были модифицированы
            headers_json = page.text_content("pre")
            assert "mocked-jwt-token" in headers_json
            assert "intercepted" in headers_json
            
            print("✅ Аутентификационные заголовки успешно перехвачены и модифицированы")
            
        finally:
            browser.close()
```

### Задание 4: Расширенная отчетность с Allure (15 баллов)

Создайте файл `test_allure_integration.py`:

```python
import pytest
import allure
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

@allure.feature("Расширенная отчетность")
@allure.story("Интеграция с Allure")
class TestAllureReporting:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page
    
    @allure.title("Тест с подробной отчетностью")
    @allure.description("Полный тест с шагами, скриншотами и attachments")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_detailed_reporting(self):
        with allure.step("Навигация на тестовую страницу"):
            self.page.goto("https://testpages.eviltester.com/styled/index.html")
            self.page.wait_for_load_state("networkidle")
            
            # Добавляем скриншот
            screenshot = self.page.screenshot()
            allure.attach(
                screenshot,
                name="Главная страница",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Взаимодействие с элементами"):
            # Кликаем по ссылке
            self.page.click("a[href*='basic-html-form']")
            
            # Заполняем форму
            self.page.fill("#username", "testuser")
            self.page.fill("#password", "testpass")
            
            # Скриншот заполненной формы
            form_screenshot = self.page.screenshot()
            allure.attach(
                form_screenshot,
                name="Заполненная форма",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Проверка результатов"):
            # Проверяем URL
            current_url = self.page.url
            allure.attach(
                current_url,
                name="Текущий URL",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert "basic-html-form" in current_url
    
    @allure.title("Тест с параметризацией")
    @allure.description("Тест с различными параметрами viewport")
    @pytest.mark.parametrize("viewport", [
        {"width": 1920, "height": 1080, "name": "desktop"},
        {"width": 768, "height": 1024, "name": "tablet"},
        {"width": 375, "height": 667, "name": "mobile"}
    ])
    def test_responsive_screenshots(self, viewport):
        # Устанавливаем viewport
        self.page.set_viewport_size(viewport)
        
        with allure.step(f"Тестирование на {viewport['name']} ({viewport['width']}x{viewport['height']})"):
            self.page.goto("https://testpages.eviltester.com/styled/index.html")
            self.page.wait_for_load_state("networkidle")
            
            # Делаем скриншот для каждого размера
            screenshot = self.page.screenshot()
            allure.attach(
                screenshot,
                name=f"Скриншот {viewport['name']}",
                attachment_type=allure.attachment_type.PNG
            )
            
            # Добавляем информацию о viewport
            viewport_info = f"Width: {viewport['width']}, Height: {viewport['height']}"
            allure.attach(
                viewport_info,
                name="Viewport Info",
                attachment_type=allure.attachment_type.TEXT
            )

@allure.feature("Производительность")
class TestPerformance:
    
    @allure.title("Тест производительности загрузки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_load_performance(self, page):
        with allure.step("Измерение времени загрузки"):
            # Начинаем измерение
            start_time = page.evaluate("() => performance.timing.navigationStart")
            
            page.goto("https://testpages.eviltester.com/styled/index.html")
            page.wait_for_load_state("networkidle")
            
            # Завершаем измерение
            end_time = page.evaluate("() => performance.timing.loadEventEnd")
            load_time = (end_time - start_time) / 1000  # в секундах
            
            allure.attach(
                str(load_time),
                name="Время загрузки (сек)",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Добавляем метрики производительности
            metrics = page.evaluate("""() => ({
                domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
                firstPaint: performance.timing.responseStart - performance.timing.navigationStart,
                loadEvent: performance.timing.loadEventEnd - performance.timing.navigationStart
            })""")
            
            allure.attach(
                str(metrics),
                name="Метрики производительности",
                attachment_type=allure.attachment_type.JSON
            )
            
            assert load_time < 10, f"Время загрузки слишком большое: {load_time} сек"

# conftest.py для Allure интеграции
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            # Добавляем скриншот при падении
            if hasattr(item.instance, 'page'):
                screenshot = item.instance.page.screenshot()
                allure.attach(
                    screenshot,
                    name=f"failure_screenshot_{datetime.now().strftime('%H-%M-%S')}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to attach screenshot: {e}")
```

## Дополнительные задания (по желанию)

### Задание 5: Интеграция с Docker и CI (20 баллов)
Создайте Dockerfile и docker-compose.yml для запуска тестов в контейнере.

### Задание 6: Custom Assertions и Matchers (15 баллов)
Реализуйте кастомные assertion функции для специфичных проверок.

### Задание 7: Тестирование PWA приложений (15 баллов)
Создайте тесты для Progressive Web Applications с offline режимом.

## Требования к отчету

1. **Титульный лист** с названием работы, ФИО, датой
2. **Цель работы** - краткое описание целей
3. **Ход работы** - по каждому заданию:
   - Код программы
   - Результаты выполнения
   - Скриншоты и диаграммы
   - Анализ производительности
4. **Выводы** - что было освоено, сложности, выводы
5. **Ответы на контрольные вопросы**

## Контрольные вопросы

1. Какие преимущества дает параллельное тестирование?
2. Как работает визуальное тестирование и когда его использовать?
3. Какие возможности предоставляет network interception?
4. Как интегрировать Playwright с системами отчетности?
5. Как обеспечить изоляцию тестов при параллельном выполнении?
6. Какие метрики производительности можно собирать?
7. Как обрабатывать flaky тесты в расширенных сценариях?
8. Какие best practices следует соблюдать при advanced автоматизации?

## Критерии оценки

- **85-100 баллов** - Все задания выполнены, код профессиональный, отчет полный
- **70-84 балла** - Основные задания выполнены, есть мелкие недочеты
- **50-69 баллов** - Выполнены базовые задания, требуется доработка
- **Менее 50 баллов** - Существенные недоработки

## Полезные ресурсы

- [Playwright Advanced Guides](https://playwright.dev/python/docs/advanced-topics)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Docker for Testing](https://docs.docker.com/language/python/)