# ❓ Часто задаваемые вопросы по расширенным возможностям Playwright

## 🚀 Расширенная автоматизация

### **Q: Зачем нужно параллельное тестирование и как его правильно реализовать?**
**A:** Параллельное тестирование позволяет значительно ускорить выполнение тестов, особенно в крупных тестовых наборах.

**Преимущества:**
✅ **Скорость** - тесты выполняются в разы быстрее
✅ **Эффективность** - лучшее использование ресурсов
✅ **Масштабируемость** - легко добавлять новые тесты
✅ **CI/CD интеграция** - идеально для pipeline

```python
# ❌ Последовательное выполнение (медленно)
def run_tests_sequential():
    for test in test_list:
        execute_test(test)  # 10 тестов × 30 сек = 5 минут

# ✅ Параллельное выполнение (быстро)
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def run_tests_parallel():
    async def run_single_test(test):
        # Каждый тест в своем контексте
        async with async_playwright() as p:
            # ... выполнение теста
            pass
    
    # Запуск 10 тестов параллельно
    tasks = [run_single_test(test) for test in test_list]
    await asyncio.gather(*tasks)  # Все тесты ~30 сек вместо 5 минут
```

**Важные моменты:**
- ❗ **Изоляция** - каждый тест должен иметь свой browser context
- ❗ **Тестовые данные** - избегать конфликтов между параллельными тестами
- ❗ **Ресурсы** - не перегружать систему (оптимально 2-4 workers per CPU core)

### **Q: Как правильно реализовать retry механизм для нестабильных тестов?**
**A:** Smart retry стратегии:

```python
import asyncio
import time
from playwright.sync_api import sync_playwright

class SmartRetryTester:
    def __init__(self, max_retries=3, base_delay=1):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def execute_with_retry(self, test_func, *args, **kwargs):
        """Smart retry с экспоненциальной задержкой"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return test_func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Экспоненциальная задержка: 1s, 2s, 4s...
                    delay = self.base_delay * (2 ** attempt)
                    print(f"Попытка {attempt + 1} провалилась, "
                          f"повтор через {delay} сек...")
                    time.sleep(delay)
                else:
                    print(f"Все {self.max_retries} попыток провалились")
        
        raise last_exception

# Использование
retry_tester = SmartRetryTester(max_retries=3)

def flaky_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto("https://flaky-site.com")
            # ... тестовая логика
        finally:
            browser.close()

# Выполнение с retry
result = retry_tester.execute_with_retry(flaky_test)
```

## 🎨 Визуальное тестирование

### **Q: Когда использовать визуальное тестирование и как его правильно настроить?**
**A:** Визуальное тестирование идеально для:

✅ **UI компонентов** - кнопки, формы, навигация
✅ **Дизайн изменений** - рефакторинг, redesign
✅ **Responsive design** - адаптивность на устройствах
✅ **Cross-browser testing** - совместимость браузеров

```python
import hashlib
from PIL import Image, ImageChops
import numpy as np

class VisualRegressionTester:
    def __init__(self, tolerance=5.0):  # Допустимое отклонение в процентах
        self.tolerance = tolerance
        self.baselines = {}
    
    def create_baseline(self, page, test_name):
        """Создать baseline скриншот"""
        screenshot_path = f"baselines/{test_name}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        self.baselines[test_name] = self._calculate_hash(screenshot_path)
        return screenshot_path
    
    def compare_visual(self, page, test_name):
        """Сравнить текущий скриншот с baseline"""
        current_path = f"current/{test_name}.png"
        baseline_path = f"baselines/{test_name}.png"
        
        # Создаем текущий скриншот
        page.screenshot(path=current_path, full_page=True)
        
        # Если baseline не существует - создаем
        if test_name not in self.baselines:
            return True, self.create_baseline(page, test_name)
        
        # Сравнение изображений
        similarity = self._compare_images(baseline_path, current_path)
        
        if similarity < (100 - self.tolerance):
            # Создаем diff изображение
            self._create_diff_image(baseline_path, current_path, 
                                  f"diffs/{test_name}_diff.png")
            return False, f"Визуальные различия: {100-similarity:.1f}%"
        
        return True, "Визуально идентично"
    
    def _compare_images(self, img1_path, img2_path):
        """Сравнение изображений с помощью PIL"""
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        
        # Проверка размеров
        if img1.size != img2.size:
            return 0
        
        # Сравнение пикселей
        diff = ImageChops.difference(img1, img2)
        diff_array = np.array(diff)
        
        # Подсчет совпадающих пикселей
        identical_pixels = np.sum(diff_array == 0)
        total_pixels = diff_array.size
        
        return (identical_pixels / total_pixels) * 100
```

### **Q: Как обрабатывать легитимные визуальные изменения?**
**A:** Система управления baselines:

```python
class BaselineManager:
    def __init__(self):
        self.approved_changes = set()
        self.pending_reviews = {}
    
    def handle_visual_difference(self, test_name, diff_percentage, diff_image_path):
        """Обработка визуальных различий"""
        
        if diff_percentage <= 2:  # Малые изменения - автоапрув
            print(f"✅ Автоапрув малых изменений: {diff_percentage}%")
            self.update_baseline(test_name)
            return True
            
        elif diff_percentage <= 10:  # Средние изменения - ревью
            print(f"⚠️  Требуется ревью: {diff_percentage}%")
            self.pending_reviews[test_name] = {
                'diff_path': diff_image_path,
                'percentage': diff_percentage,
                'timestamp': time.time()
            }
            return self.request_review(test_name)
            
        else:  # Большие изменения - отклонение
            print(f"❌ Большие изменения, требуются исправления: {diff_percentage}%")
            return False
    
    def approve_change(self, test_name):
        """Апрув изменений после ревью"""
        if test_name in self.pending_reviews:
            self.update_baseline(test_name)
            del self.pending_reviews[test_name]
            print(f"✅ Изменения апрувнуты: {test_name}")
```

## 🌐 Network Interception

### **Q: Как эффективно использовать network interception для тестирования?**
**A:** Мощные сценарии для network interception:

```python
def advanced_network_testing():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 1. Мокирование медленной сети
        def simulate_slow_network(route):
            # Добавляем искусственную задержку
            import time
            time.sleep(2)  # 2 секунды задержки
            route.continue_()
        
        page.route("**/api/**", simulate_slow_network)
        
        # 2. Мокирование API ответов
        def mock_api_responses(route, request):
            if "/users" in request.url:
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    headers={"X-Mocked": "true"},
                    body=json.dumps([
                        {"id": 1, "name": "Mocked User 1"},
                        {"id": 2, "name": "Mocked User 2"}
                    ])
                )
            elif "/error" in request.url:
                route.fulfill(status=500, body="Internal Server Error")
            else:
                route.continue_()
        
        page.route("**/api/**", mock_api_responses)
        
        # 3. Блокировка трекеров и рекламы
        blocked_domains = ['google-analytics.com', 'facebook.com', 'adservice']
        
        def block_trackers(route, request):
            if any(domain in request.url for domain in blocked_domains):
                route.abort()
            else:
                route.continue_()
        
        page.route("**/*", block_trackers)
        
        # 4. Модификация запросов
        def modify_requests(route, request):
            # Добавляем custom headers
            headers = {
                **request.headers,
                "X-Test-Environment": "staging",
                "X-Feature-Flag": "new-ui-enabled"
            }
            route.continue_(headers=headers)
        
        page.route("**/graphql", modify_requests)
```

### **Q: Как тестировать offline режим приложения?**
**A:** 

```python
def test_offline_functionality():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        
        # Навигация онлайн
        page.goto("https://progressive-app.com")
        page.wait_for_load_state("networkidle")
        
        # Сохраняем важные данные в cache
        page.evaluate("""() => {
            // Сохраняем критичные данные
            localStorage.setItem('userPreferences', JSON.stringify({
                theme: 'dark',
                language: 'en'
            }));
        }""")
        
        # Переводим в offline режим
        context.set_offline(True)
        
        try:
            # Тестируем offline функциональность
            page.reload()
            
            # Проверяем, что приложение работает offline
            offline_content = page.text_content("#offline-status")
            assert "Offline mode" in offline_content
            
            # Тестируем кэшированные данные
            user_prefs = page.evaluate("() => localStorage.getItem('userPreferences')")
            assert user_prefs is not None
            
            # Проверяем Service Worker
            sw_ready = page.evaluate("() => navigator.serviceWorker.controller !== null")
            assert sw_ready, "Service Worker должен быть активен"
            
        finally:
            # Возвращаем online
            context.set_offline(False)
```

## 📊 Расширенная отчетность

### **Q: Как интегрировать Playwright с системами отчетности типа Allure?**
**A:** Комплексная интеграция с Allure:

```python
import allure
import pytest
from datetime import datetime

@allure.feature("Advanced Testing")
@allure.story("Performance Monitoring")
class TestAdvancedReporting:
    
    @allure.title("Комплексный тест с метриками")
    @allure.description("""
    Тест включает:
    - Множественные скриншоты
    - Метрики производительности
    - Network logs
    - Console logs
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("performance", "regression")
    def test_comprehensive_metrics(self, page):
        
        # Сбор метрик производительности
        with allure.step("Измерение Core Web Vitals"):
            page.goto("https://example.com")
            
            # First Contentful Paint
            fcp = page.evaluate("""() => 
                performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0
            """)
            
            # Largest Contentful Paint  
            lcp = page.evaluate("""() => {
                const entries = performance.getEntriesByType('largest-contentful-paint');
                return entries[entries.length - 1]?.startTime || 0;
            }""")
            
            # Cumulative Layout Shift
            cls = page.evaluate("""() => {
                let cls = 0;
                new PerformanceObserver((entryList) => {
                    for (const entry of entryList.getEntries()) {
                        if (!entry.hadRecentInput) {
                            cls += entry.value;
                        }
                    }
                }).observe({type: 'layout-shift', buffered: true});
                return cls;
            }""")
            
            # Прикрепляем метрики
            allure.attach(
                str({"FCP": fcp, "LCP": lcp, "CLS": cls}),
                name="Core Web Vitals",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Анализ network активности"):
            # Сбор network информации
            network_logs = []
            page.on("response", lambda response: network_logs.append({
                "url": response.url,
                "status": response.status,
                "size": len(response.body() if response.body else b""),
                "timing": response.request.timing
            }))
            
            page.goto("https://complex-site.com")
            
            # Анализ lent ресурсов
            large_resources = [r for r in network_logs if r["size"] > 100000]  # > 100KB
            
            allure.attach(
                str(len(large_resources)),
                name="Large Resources Count",
                attachment_type=allure.attachment_type.TEXT
            )
            
            if large_resources:
                allure.attach(
                    str([r["url"] for r in large_resources[:5]]),
                    name="Top Large Resources",
                    attachment_type=allure.attachment_type.JSON
                )
```

### **Q: Как создавать custom dashboards для мониторинга тестов?**
**A:** 

```python
import json
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

class TestAnalyticsDashboard:
    def __init__(self, db_path="test_analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_runs (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME,
                test_name TEXT,
                status TEXT,
                duration REAL,
                browser TEXT,
                viewport TEXT,
                flaky BOOLEAN
            )
        """)
        
        conn.commit()
        conn.close()
    
    def record_test_result(self, test_info):
        """Запись результата теста"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO test_runs 
            (timestamp, test_name, status, duration, browser, viewport, flaky)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(),
            test_info["name"],
            test_info["status"],
            test_info["duration"],
            test_info["browser"],
            test_info["viewport"],
            test_info.get("flaky", False)
        ))
        
        conn.commit()
        conn.close()
    
    def generate_dashboard(self):
        """Генерация dashboard"""
        conn = sqlite3.connect(self.db_path)
        
        # Статистика по статусам
        status_stats = pd.read_sql("""
            SELECT status, COUNT(*) as count, AVG(duration) as avg_duration
            FROM test_runs 
            GROUP BY status
        """, conn)
        
        # Trend по времени
        trend_data = pd.read_sql("""
            SELECT DATE(timestamp) as date, 
                   COUNT(*) as total_tests,
                   AVG(CASE WHEN status = 'PASSED' THEN 1.0 ELSE 0 END) as pass_rate
            FROM test_runs 
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
            LIMIT 30
        """, conn)
        
        # Создание графиков
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Pie chart статусов
        axes[0,0].pie(status_stats['count'], labels=status_stats['status'], autopct='%1.1f%%')
        axes[0,0].set_title('Распределение статусов тестов')
        
        # 2. Pass rate trend
        axes[0,1].plot(trend_data['date'], trend_data['pass_rate'])
        axes[0,1].set_title('Trend успешности тестов')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Duration distribution
        duration_data = pd.read_sql("SELECT duration FROM test_runs WHERE status = 'PASSED'", conn)
        axes[1,0].hist(duration_data['duration'], bins=50)
        axes[1,0].set_title('Распределение времени выполнения')
        axes[1,0].set_xlabel('Время (сек)')
        
        # 4. Flaky tests analysis
        flaky_data = pd.read_sql("""
            SELECT test_name, COUNT(*) as run_count,
                   SUM(CASE WHEN flaky THEN 1 ELSE 0 END) as flaky_count
            FROM test_runs 
            GROUP BY test_name
            HAVING run_count > 5
        """, conn)
        
        if not flaky_data.empty:
            flaky_data['flaky_rate'] = flaky_data['flaky_count'] / flaky_data['run_count']
            axes[1,1].bar(range(len(flaky_data)), flaky_data['flaky_rate'])
            axes[1,1].set_title('Flaky тесты')
            axes[1,1].set_xticks(range(len(flaky_data)))
            axes[1,1].set_xticklabels(flaky_data['test_name'], rotation=45)
        
        plt.tight_layout()
        plt.savefig('test_dashboard.png', dpi=300, bbox_inches='tight')
        conn.close()
        
        return 'test_dashboard.png'

# Использование в тестах
dashboard = TestAnalyticsDashboard()

def pytest_runtest_logreport(report):
    """Hook для записи результатов в dashboard"""
    if report.when == "call":
        test_info = {
            "name": report.nodeid,
            "status": report.outcome.upper(),
            "duration": report.duration,
            "browser": "chromium",  # или динамически определять
            "viewport": "1920x1080",
            "flaky": hasattr(report, 'wasxfail')
        }
        dashboard.record_test_result(test_info)
```

## ⚡ Производительность и оптимизация

### **Q: Как оптимизировать производительность тестов при масштабировании?**
**A:** 

```python
class PerformanceOptimizer:
    def __init__(self):
        self.browser_pool = {}
        self.page_cache = {}
    
    async def optimize_test_execution(self, test_configs):
        """Оптимизированное параллельное выполнение"""
        
        # 1. Pool браузеров с переиспользованием
        async def get_browser_pool(size=4):
            browsers = []
            for i in range(size):
                browser = await p.chromium.launch(
                    args=['--disable-dev-shm-usage']  # Оптимизация памяти
                )
                browsers.append(browser)
            return browsers
        
        # 2. Кэширование часто используемых страниц
        async def create_page_cache(browser, urls):
            pages = {}
            for url in urls:
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle")
                pages[url] = page
            return pages
        
        # 3. Batch processing с оптимальной нагрузкой
        async def process_test_batch(test_batch, browser):
            results = []
            semaphore = asyncio.Semaphore(2)  # Ограничиваем concurrency
            
            async def process_single_test(test_config):
                async with semaphore:
                    context = await browser.new_context()
                    page = await context.new_page()
                    
                    try:
                        # Выполнение теста
                        result = await execute_test(page, test_config)
                        results.append(result)
                    finally:
                        await page.close()
                        await context.close()
            
            # Параллельная обработка batch
            tasks = [process_single_test(config) for config in test_batch]
            await asyncio.gather(*tasks)
            
            return results
        
        # 4. Memory management
        async def monitor_resources():
            import psutil
            process = psutil.Process()
            
            while True:
                memory_mb = process.memory_info().rss / 1024 / 1024
                cpu_percent = process.cpu_percent()
                
                if memory_mb > 1000:  # > 1GB
                    print(f"⚠️  Высокое потребление памяти: {memory_mb:.1f} MB")
                    # Принудительная очистка
                    await self.cleanup_old_contexts()
                
                await asyncio.sleep(30)  # Проверка каждые 30 секунд
```

## 🔧 Troubleshooting

### **Q: Как диагностировать и решать проблемы с flaky тестами?**
**A:** Systematic approach к flaky тестам:

```python
class FlakyTestAnalyzer:
    def __init__(self):
        self.flaky_patterns = {}
        self.execution_history = []
    
    def analyze_flaky_test(self, test_func, iterations=10):
        """Комплексный анализ flaky теста"""
        
        results = []
        timing_data = []
        
        for i in range(iterations):
            start_time = time.time()
            
            try:
                result = test_func()
                execution_time = time.time() - start_time
                results.append({"iteration": i, "status": "PASSED", 
                              "time": execution_time, "result": result})
                timing_data.append(execution_time)
                
            except Exception as e:
                execution_time = time.time() - start_time
                results.append({"iteration": i, "status": "FAILED",
                              "time": execution_time, "error": str(e)})
                timing_data.append(execution_time)
        
        # Анализ результатов
        pass_rate = sum(1 for r in results if r["status"] == "PASSED") / len(results)
        avg_time = sum(timing_data) / len(timing_data)
        time_variance = statistics.variance(timing_data) if len(timing_data) > 1 else 0
        
        analysis = {
            "pass_rate": pass_rate,
            "average_time": avg_time,
            "time_variance": time_variance,
            "consistent_failures": self._find_failure_patterns(results),
            "timing_issues": time_variance > (avg_time * 0.5)  # Высокая вариативность
        }
        
        return analysis, results
    
    def _find_failure_patterns(self, results):
        """Поиск паттернов падений"""
        failures = [r for r in results if r["status"] == "FAILED"]
        if not failures:
            return []
        
        # Анализ частоты падений
        failure_frequency = len(failures) / len(results)
        
        # Анализ последовательности
        consecutive_failures = 0
        max_consecutive = 0
        for result in results:
            if result["status"] == "FAILED":
                consecutive_failures += 1
                max_consecutive = max(max_consecutive, consecutive_failures)
            else:
                consecutive_failures = 0
        
        return {
            "frequency": failure_frequency,
            "max_consecutive": max_consecutive,
            "common_errors": self._extract_common_errors(failures)
        }
```

---

## 🆘 Нужна помощь?

**Дополнительные ресурсы:**
- [Playwright Advanced Patterns](https://playwright.dev/python/docs/test-runners)
- [Performance Testing Guide](https://web.dev/vitals/)
- [Visual Testing Best Practices](https://applitools.com/blog/visual-testing-best-practices/)
- [CI/CD Integration Examples](https://github.com/microsoft/playwright/tree/main/examples)

**Professional Tips:**
1. **Начинайте с простого** - постепенно добавляйте сложность
2. **Мониторьте ресурсы** - память, CPU, network
3. **Документируйте паттерны** - создавайте knowledge base
4. **Автоматизируйте рутину** - scripts для повторяющихся задач
5. **Измеряйте эффект** - track before/after метрики

**Помните:** Расширенные возможности - это инструменты для решения конкретных задач, а не цель сами по себе!