# ❓ Часто задаваемые вопросы по Playwright

## 🎭 Основы Playwright

### **Q: Чем Playwright отличается от Selenium?**
**A:** Playwright - это более современный и мощный инструмент:

| Особенность | Selenium | Playwright |
|-------------|----------|------------|
| **Архитектура** | WebDriver протокол | Собственный протокол |
| **Скорость** | Средняя | Очень высокая |
| **Ожидания** | Нужно явно ждать | Автоматические ожидания |
| **Браузеры** | Chrome, Firefox, Safari | Chromium, Firefox, WebKit |
| **Mobile** | Через Appium | Встроенная эмуляция |
| **API** | Более verbose | Интуитивный и лаконичный |

```python
# Selenium - требуется много ожиданий
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, "button")))
element.click()

# Playwright - автоматические ожидания
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    page.click("#button")  # Автоматически ждет элемент
```

### **Q: Когда использовать sync API, а когда async API?**
**A:** 

**Sync API** ✅ (рекомендуется для начинающих):
- Проще для понимания
- Последовательное выполнение
- Подходит для большинства тестов

```python
from playwright.sync_api import sync_playwright

def test_sync_example():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        title = page.title()
        browser.close()
```

**Async API** ✅ (для продвинутых сценариев):
- Высокая производительность
- Параллельное выполнение
- Подходит для нагрузочного тестирования

```python
import asyncio
from playwright.async_api import async_playwright

async def test_async_example():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        title = await page.title()
        await browser.close()

# Запуск
asyncio.run(test_async_example())
```

### **Q: Как правильно выбирать селекторы в Playwright?**
**A:** Иерархия предпочтений:

```python
# ✅ Лучшие варианты (по приоритету):

# 1. Role-based selectors (доступность)
page.click("button[role='submit']")
page.fill("input[aria-label='Email']", "user@example.com")

# 2. Data-testid (специально для тестов)
page.click("[data-testid='login-button']")
page.fill("[data-testid='email-input']", "user@example.com")

# 3. ID selectors
page.click("#submit-btn")
page.fill("#email", "user@example.com")

# 4. Text selectors
page.click("text=Submit Form")
page.click("'Login'")  # точное совпадение

# 5. CSS selectors (когда других нет)
page.click(".form-group:nth-child(2) button.primary")

# ❌ Избегать:
page.click("//div[@class='container']/div[3]/button")  # XPath - хрупкий
page.click("div > div > div > button")  # Сложные CSS - ненадежные
```

## 🎯 Практические сценарии

### **Q: Как тестировать загрузку файлов?**
**A:** Playwright отлично с этим справляется:

```python
def test_file_upload():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("https://example.com/upload")
        
        # Простая загрузка
        page.set_input_files("#file-upload", "path/to/file.pdf")
        
        # Множественная загрузка
        page.set_input_files("#multi-upload", [
            "file1.pdf",
            "file2.docx",
            "file3.jpg"
        ])
        
        # Drag & Drop загрузка
        with page.expect_file_chooser() as fc_info:
            page.click("#drop-zone")
        file_chooser = fc_info.value
        file_chooser.set_files("document.pdf")
        
        page.click("#submit")
        expect(page.locator(".success")).to_be_visible()
```

### **Q: Как работать с popup окнами и alerts?**
**A:** 

```python
def test_popup_handling():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Обработка JavaScript alert
        page.on("dialog", lambda dialog: dialog.accept())
        page.evaluate("alert('Hello')")
        
        # Обработка confirm
        page.on("dialog", lambda dialog: dialog.accept())  # или dialog.dismiss()
        page.evaluate("confirm('Are you sure?')")
        
        # Обработка prompt
        page.on("dialog", lambda dialog: dialog.accept("User input"))
        result = page.evaluate("prompt('Enter your name:')")
        
        # Popup окна (новые вкладки)
        with page.context.expect_page() as popup_info:
            page.click("#open-popup-link")
        popup = popup_info.value
        popup.wait_for_load_state()
        assert "popup" in popup.title().lower()
```

### **Q: Как тестировать мобильные версии сайтов?**
**A:** Встроенная эмуляция устройств:

```python
def test_mobile_version():
    with sync_playwright() as p:
        # Использование готовых устройств
        iphone = p.devices["iPhone 12 Pro"]
        browser = p.chromium.launch()
        context = browser.new_context(**iphone)
        page = context.new_page()
        
        page.goto("https://example.com")
        # Сайт отображается как на iPhone
        
        # Кастомная эмуляция
        custom_mobile = {
            "user_agent": "Custom Mobile Browser",
            "viewport": {"width": 375, "height": 667},
            "device_scale_factor": 2,
            "is_mobile": True,
            "has_touch": True
        }
        
        context = browser.new_context(**custom_mobile)
        page = context.new_page()
        page.goto("https://whatismyviewport.com/")
```

## 🌐 Сетевые возможности

### **Q: Как перехватывать и модифицировать сетевые запросы?**
**A:** Мощные возможности route interception:

```python
def test_network_interception():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Блокировка запросов
        page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
        
        # Модификация запросов
        def handle_route(route):
            if "api/user" in route.request.url:
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body='{"name": "Mock User", "id": 123}'
                )
            else:
                route.continue_()
        
        page.route("**/api/**", handle_route)
        
        # Мониторинг запросов
        page.on("request", lambda request: print(f"Request: {request.method} {request.url}"))
        page.on("response", lambda response: print(f"Response: {response.status} {response.url}"))
        
        page.goto("https://example.com")
```

### **Q: Как работать с cookies и сессиями?**
**A:**

```python
def test_cookies_and_sessions():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Работа с cookies
        context = browser.new_context()
        page = context.new_page()
        
        # Установка cookies
        context.add_cookies([{
            "name": "session_token",
            "value": "abc123",
            "domain": "example.com",
            "path": "/",
            "expires": -1,  # Session cookie
            "httpOnly": True,
            "secure": True
        }])
        
        # Получение cookies
        cookies = context.cookies()
        print(cookies)
        
        # Сохранение и восстановление состояния
        storage_state = context.storage_state()
        
        # В новом контексте
        new_context = browser.new_context(storage_state=storage_state)
        new_page = new_context.new_page()
        # Пользователь уже авторизован
```

## 🎨 Advanced Features

### **Q: Как тестировать визуальные изменения (Visual Testing)?**
**A:** С помощью скриншотов:

```python
def test_visual_regression():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("https://example.com")
        
        # Скриншот всей страницы
        page.screenshot(path="full_page.png", full_page=True)
        
        # Скриншот конкретного элемента
        page.locator(".hero-section").screenshot(path="hero.png")
        
        # Сравнение скриншотов (базовая реализация)
        import hashlib
        def get_image_hash(image_path):
            with open(image_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        
        # Сохраняем baseline
        page.screenshot(path="baseline.png")
        baseline_hash = get_image_hash("baseline.png")
        
        # Проверка после изменений
        page.screenshot(path="current.png")
        current_hash = get_image_hash("current.png")
        
        assert baseline_hash == current_hash, "Визуальные изменения обнаружены!"
```

### **Q: Как реализовать параллельное тестирование?**
**A:**

```python
import concurrent.futures
from playwright.sync_api import sync_playwright

def run_single_test(test_data):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto(test_data["url"])
            page.fill("#search", test_data["query"])
            page.click("#submit")
            assert test_data["expected"] in page.text_content("#results")
            return True
        except Exception as e:
            return False
        finally:
            browser.close()

def test_parallel_execution():
    test_cases = [
        {"url": "https://site1.com", "query": "test1", "expected": "result1"},
        {"url": "https://site2.com", "query": "test2", "expected": "result2"},
        {"url": "https://site3.com", "query": "test3", "expected": "result3"},
    ]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(run_single_test, test_cases))
    
    assert all(results), "Некоторые тесты провалились"
```

## 🔧 Debugging и Troubleshooting

### **Q: Как отлаживать упавшие тесты?**
**A:** Мощные инструменты диагностики:

```python
def test_with_debugging():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Визуальный режим
            slow_mo=1000     # Замедление для наблюдения
        )
        page = browser.new_page()
        
        try:
            page.goto("https://example.com")
            
            # Пауза для ручной отладки
            page.pause()  # Playwright Inspector откроется
            
            # Логирование всех действий
            page.on("console", lambda msg: print(f"Console: {msg.text}"))
            page.on("pageerror", lambda exc: print(f"Page Error: {exc}"))
            page.on("request", lambda req: print(f"Request: {req.method} {req.url}"))
            page.on("response", lambda res: print(f"Response: {res.status} {res.url}"))
            
            page.click("#problematic-button")
            
        except Exception as e:
            # Скриншот при ошибке
            page.screenshot(path="error_screenshot.png")
            # HTML страницы для анализа
            with open("page_content.html", "w") as f:
                f.write(page.content())
            raise
```

### **Q: Как обрабатывать flaky тесты?**
**A:** Стратегии стабилизации:

```python
import time
from playwright.sync_api import sync_playwright, expect

def robust_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Retry mechanism
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                page.goto("https://flaky-site.com")
                
                # Явные ожидания вместо sleep
                expect(page.locator("#dynamic-content")).to_be_visible(timeout=10000)
                
                # Проверка нескольких условий
                expect(page).to_have_title("Expected Title")
                expect(page.locator(".success-message")).to_contain_text("Operation completed")
                
                break  # Успешно завершено
                
            except AssertionError:
                if attempt == max_attempts - 1:
                    raise  # Последняя попытка - падаем
                print(f"Попытка {attempt + 1} провалилась, повторяем...")
                time.sleep(2)  # Небольшая пауза перед retry
```

## ⚡ Производительность

### **Q: Как оптимизировать скорость выполнения тестов?**
**A:** 

```python
def optimized_test_setup():
    with sync_playwright() as p:
        # Переиспользование браузера
        browser = p.chromium.launch()
        
        # Параллельные контексты
        contexts = []
        for i in range(3):
            context = browser.new_context()
            contexts.append(context)
        
        # Кэширование состояния
        base_context = browser.new_context()
        base_page = base_context.new_page()
        base_page.goto("https://auth-required-site.com")
        # Выполняем авторизацию один раз
        base_page.fill("#username", "user")
        base_page.fill("#password", "pass")
        base_page.click("#login")
        
        # Сохраняем авторизованное состояние
        storage = base_context.storage_state()
        
        # Используем в других тестах
        new_context = browser.new_context(storage_state=storage)
        new_page = new_context.new_page()
        # Уже авторизован!
```

## 🛡️ Безопасность

### **Q: Как тестировать security аспекты?**
**A:**

```python
def test_security_features():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        # Тестирование CSP
        page.route("**/*", lambda route: route.continue_(headers={
            "Content-Security-Policy": "default-src 'self'"
        }))
        
        # Тестирование XSS
        malicious_input = "<script>alert('XSS')</script>"
        page.fill("#comment", malicious_input)
        page.click("#submit")
        
        # Проверка, что скрипт не выполнился
        assert "alert" not in page.content()
        
        # Тестирование CSRF
        page.set_extra_http_headers({
            "Origin": "https://malicious-site.com"
        })
        # Проверка отклонения запроса
```

---

## 🆘 Нужна помощь?

**Полезные ресурсы:**
- [Официальная документация](https://playwright.dev/python/)
- [Playwright Inspector](https://playwright.dev/python/docs/debug)
- [Community Discord](https://aka.ms/playwright/discord)
- [GitHub Issues](https://github.com/microsoft/playwright/issues)

**Best Practices:**
1. Всегда используйте автоматические ожидания
2. Предпочитайте role-based и data-testid селекторы
3. Тестируйте на нескольких браузерах
4. Используйте Page Object Model для сложных тестов
5. Включайте визуальное тестирование для критичных UI элементов