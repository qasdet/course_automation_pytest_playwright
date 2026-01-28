# 📋 Шаблоны тестов Playwright

## 🎯 Базовые шаблоны

### **Конфигурационный файл**

```python
# playwright.config.py
from playwright.sync_api import ViewportSize

config = {
    # Базовые настройки
    "base_url": "https://your-app.com",
    "timeout": 30000,
    "navigation_timeout": 30000,
    
    # Браузерные настройки
    "browsers": ["chromium", "firefox", "webkit"],
    "headless": False,
    "slow_mo": 1000,
    
    # Viewport и устройства
    "viewport": ViewportSize(width=1920, height=1080),
    "devices": ["Desktop Chrome", "iPhone 12", "Pixel 5"],
    
    # CI/CD настройки
    "ci_headless": True,
    "ci_workers": 4,
    "retry_attempts": 2,
    
    # Отчетность
    "screenshot_on_failure": True,
    "video_on_failure": True,
    "trace_on_failure": True,
    
    # Тестовые данные
    "test_data_path": "./test_data/",
    "screenshots_path": "./screenshots/",
    "videos_path": "./videos/",
    "traces_path": "./traces/"
}
```

### **Базовый тестовый класс**

```python
# base_test.py
import pytest
from playwright.sync_api import sync_playwright, expect, Page, BrowserContext
from typing import Generator
import logging
from datetime import datetime

class BasePlaywrightTest:
    """Базовый класс для Playwright тестов"""
    
    @pytest.fixture(scope="class")
    def playwright_instance(self) -> Generator[sync_playwright, None, None]:
        """Фикстура для Playwright инстанса"""
        with sync_playwright() as p:
            yield p
    
    @pytest.fixture
    def browser(self, playwright_instance, request):
        """Фикстура для браузера"""
        browser_type = getattr(playwright_instance, request.param)
        browser = browser_type.launch(
            headless=request.config.getoption("--headless", False),
            slow_mo=request.config.getoption("--slowmo", 0)
        )
        yield browser
        browser.close()
    
    @pytest.fixture
    def context(self, browser, request):
        """Фикстура для browser context"""
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="Europe/London"
        )
        yield context
        context.close()
    
    @pytest.fixture
    def page(self, context) -> Page:
        """Фикстура для страницы"""
        page = context.new_page()
        page.set_default_timeout(30000)
        yield page
    
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'test_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )

# Параметризация браузеров
pytestmark = pytest.mark.parametrize("browser", ["chromium", "firefox", "webkit"], indirect=True)
```

## 🎨 Page Object шаблоны

### **Базовый Page Object**

```python
# pages/base_page.py
from playwright.sync_api import Page, Locator, expect
from typing import Union, List

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000
    
    def navigate(self, url: str) -> None:
        """Навигация на страницу"""
        self.page.goto(url, wait_until="networkidle")
    
    def get_element(self, selector: str) -> Locator:
        """Получить элемент по селектору"""
        return self.page.locator(selector)
    
    def click_element(self, selector: str, timeout: int = None) -> None:
        """Кликнуть по элементу"""
        self.get_element(selector).click(timeout=timeout or self.timeout)
    
    def fill_field(self, selector: str, value: str, timeout: int = None) -> None:
        """Заполнить поле ввода"""
        self.get_element(selector).fill(value, timeout=timeout or self.timeout)
    
    def get_text(self, selector: str, timeout: int = None) -> str:
        """Получить текст элемента"""
        return self.get_element(selector).text_content(timeout=timeout or self.timeout)
    
    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """Проверить видимость элемента"""
        try:
            expect(self.get_element(selector)).to_be_visible(timeout=timeout or self.timeout)
            return True
        except:
            return False
    
    def wait_for_element(self, selector: str, timeout: int = None) -> None:
        """Ждать появления элемента"""
        expect(self.get_element(selector)).to_be_visible(timeout=timeout or self.timeout)
    
    def get_screenshot(self, filename: str = None) -> bytes:
        """Сделать скриншот"""
        if filename:
            return self.page.screenshot(path=filename, full_page=True)
        return self.page.screenshot(full_page=True)
    
    def get_current_url(self) -> str:
        """Получить текущий URL"""
        return self.page.url
    
    def get_title(self) -> str:
        """Получить заголовок страницы"""
        return self.page.title()

class FormPage(BasePage):
    """Базовый класс для страниц с формами"""
    
    def submit_form(self, submit_selector: str = "button[type='submit']") -> None:
        """Отправить форму"""
        self.click_element(submit_selector)
    
    def validate_form_errors(self, error_selector: str = ".error") -> List[str]:
        """Получить ошибки формы"""
        error_elements = self.get_element(error_selector).all()
        return [error.text_content() for error in error_elements]
    
    def is_form_valid(self) -> bool:
        """Проверить валидность формы"""
        return not self.is_visible(".error")
```

### **Конкретная страница**

```python
# pages/login_page.py
from pages.base_page import BasePage
from typing import Optional

class LoginPage(BasePage):
    """Page Object для страницы логина"""
    
    # Селекторы
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-btn"
    ERROR_MESSAGE = ".error-message"
    FORGOT_PASSWORD_LINK = "a[href='/forgot-password']"
    REMEMBER_ME_CHECKBOX = "#remember-me"
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "/login"
    
    def navigate_to_login(self, base_url: str) -> None:
        """Перейти на страницу логина"""
        self.navigate(base_url + self.url)
    
    def enter_credentials(self, username: str, password: str) -> None:
        """Ввести учетные данные"""
        self.fill_field(self.USERNAME_INPUT, username)
        self.fill_field(self.PASSWORD_INPUT, password)
    
    def click_login(self) -> 'DashboardPage':
        """Нажать кнопку логина"""
        self.click_element(self.LOGIN_BUTTON)
        return DashboardPage(self.page)
    
    def login(self, username: str, password: str, base_url: str) -> 'DashboardPage':
        """Полный процесс логина"""
        self.navigate_to_login(base_url)
        self.enter_credentials(username, password)
        return self.click_login()
    
    def get_error_message(self) -> Optional[str]:
        """Получить сообщение об ошибке"""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def click_forgot_password(self) -> 'ForgotPasswordPage':
        """Нажать ссылку восстановления пароля"""
        self.click_element(self.FORGOT_PASSWORD_LINK)
        return ForgotPasswordPage(self.page)
    
    def toggle_remember_me(self) -> None:
        """Переключить чекбокс запомнить меня"""
        self.click_element(self.REMEMBER_ME_CHECKBOX)
    
    def is_login_enabled(self) -> bool:
        """Проверить, активна ли кнопка логина"""
        return self.get_element(self.LOGIN_BUTTON).is_enabled()

# pages/dashboard_page.py
class DashboardPage(BasePage):
    """Page Object для дашборда"""
    
    USER_MENU = "#user-menu"
    LOGOUT_BUTTON = "#logout-btn"
    NOTIFICATIONS_COUNT = ".notifications-badge"
    WELCOME_MESSAGE = "h1:has-text('Welcome')"
    PROJECT_LIST = ".project-item"
    
    def is_loaded(self) -> bool:
        """Проверить загрузку страницы"""
        return self.is_visible(self.WELCOME_MESSAGE)
    
    def get_notifications_count(self) -> int:
        """Получить количество уведомлений"""
        if self.is_visible(self.NOTIFICATIONS_COUNT):
            count_text = self.get_text(self.NOTIFICATIONS_COUNT)
            return int(count_text) if count_text.isdigit() else 0
        return 0
    
    def logout(self) -> LoginPage:
        """Выполнить выход"""
        self.click_element(self.USER_MENU)
        self.click_element(self.LOGOUT_BUTTON)
        return LoginPage(self.page)
```

## 🧪 Шаблоны тестов

### **Тест авторизации**

```python
# tests/test_authentication.py
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestAuthentication:
    """Тесты аутентификации"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page, base_url):
        self.page = page
        self.base_url = base_url
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
    
    def test_successful_login(self):
        """Тест успешной авторизации"""
        # Arrange
        username = "testuser@example.com"
        password = "correct_password"
        
        # Act
        dashboard = self.login_page.login(username, password, self.base_url)
        
        # Assert
        assert dashboard.is_loaded()
        assert self.base_url in dashboard.get_current_url()
        assert "dashboard" in dashboard.get_current_url()
    
    def test_invalid_credentials(self):
        """Тест неверных учетных данных"""
        # Arrange
        username = "wrong@example.com"
        password = "wrong_password"
        
        # Act
        self.login_page.navigate_to_login(self.base_url)
        self.login_page.enter_credentials(username, password)
        self.login_page.click_login()
        
        # Assert
        error_message = self.login_page.get_error_message()
        assert error_message is not None
        assert "Invalid credentials" in error_message
    
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "password", "Username is required"),
        ("user@example.com", "", "Password is required"),
        ("", "", "Username is required"),
    ])
    def test_required_fields_validation(self, username, password, expected_error):
        """Тест валидации обязательных полей"""
        # Arrange & Act
        self.login_page.navigate_to_login(self.base_url)
        self.login_page.enter_credentials(username, password)
        self.login_page.click_login()
        
        # Assert
        error_message = self.login_page.get_error_message()
        assert error_message is not None
        assert expected_error in error_message
```

### **Тест форм**

```python
# tests/test_forms.py
import pytest
from pages.registration_page import RegistrationPage
from data.test_data import UserData

class TestForms:
    """Тесты форм"""
    
    @pytest.fixture
    def registration_page(self, page, base_url):
        page.goto(f"{base_url}/register")
        return RegistrationPage(page)
    
    def test_complete_registration(self, registration_page):
        """Тест полной регистрации"""
        # Arrange
        user_data = UserData.generate_valid_user()
        
        # Act
        confirmation_page = registration_page.register_user(user_data)
        
        # Assert
        assert confirmation_page.is_registration_successful()
        assert user_data.email in confirmation_page.get_confirmation_message()
    
    def test_duplicate_email_registration(self, registration_page):
        """Тест регистрации с дубликатом email"""
        # Arrange
        existing_email = "used@example.com"
        
        # Act
        registration_page.fill_email(existing_email)
        registration_page.submit_form()
        
        # Assert
        error = registration_page.get_email_error()
        assert "Email already registered" in error
```

### **API тесты**

```python
# tests/test_api.py
import pytest
import json
from api.client import APIClient

class TestAPI:
    """Тесты API"""
    
    @pytest.fixture
    def api_client(self):
        return APIClient(base_url="https://api.example.com")
    
    def test_get_user_success(self, api_client):
        """Тест получения пользователя"""
        # Act
        response = api_client.get("/users/1")
        
        # Assert
        assert response.status == 200
        user_data = response.json()
        assert user_data["id"] == 1
        assert "name" in user_data
    
    def test_create_user_validation(self, api_client):
        """Тест валидации создания пользователя"""
        # Arrange
        invalid_data = {"name": ""}  # Пустое имя
        
        # Act
        response = api_client.post("/users", json=invalid_data)
        
        # Assert
        assert response.status == 400
        error_data = response.json()
        assert "name" in error_data["errors"]
    
    @pytest.mark.parametrize("endpoint,expected_status", [
        ("/users", 200),
        ("/posts", 200),
        ("/comments", 200),
        ("/nonexistent", 404),
    ])
    def test_endpoints_availability(self, api_client, endpoint, expected_status):
        """Тест доступности эндпоинтов"""
        response = api_client.get(endpoint)
        assert response.status == expected_status
```

## 🎭 Advanced Patterns

### **Контекстный менеджер для тестов**

```python
# utils/test_context.py
from contextlib import contextmanager
from playwright.sync_api import Page
import allure

@contextmanager
def test_step(name: str, page: Page = None):
    """Контекстный менеджер для шагов теста"""
    try:
        if page:
            # Делаем скриншот до шага
            page.screenshot(path=f"before_{name.replace(' ', '_')}.png")
        
        with allure.step(name):
            yield
            
    except Exception as e:
        if page:
            # Скриншот при ошибке
            page.screenshot(path=f"error_{name.replace(' ', '_')}.png")
        raise

@contextmanager
def authenticated_user(page: Page, credentials: dict):
    """Контекстный менеджер для авторизованного пользователя"""
    # Логин
    page.goto("/login")
    page.fill("#username", credentials["username"])
    page.fill("#password", credentials["password"])
    page.click("#login-btn")
    
    try:
        yield page
    finally:
        # Логаут
        page.click("#user-menu")
        page.click("#logout-btn")
```

### **Data-driven тесты**

```python
# tests/test_data_driven.py
import pytest
import yaml
from pathlib import Path

def load_test_data(filename: str):
    """Загрузить тестовые данные из YAML"""
    data_path = Path(__file__).parent.parent / "test_data" / filename
    with open(data_path, 'r') as file:
        return yaml.safe_load(file)

class TestDataDriven:
    """Data-driven тесты"""
    
    @pytest.mark.parametrize("test_case", load_test_data("login_test_cases.yaml"))
    def test_login_scenarios(self, page, base_url, test_case):
        """Тест различных сценариев логина"""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate_to_login(base_url)
        login_page.enter_credentials(
            test_case["username"],
            test_case["password"]
        )
        login_page.click_login()
        
        # Assert
        if test_case["expected_success"]:
            assert "dashboard" in page.url
        else:
            error_msg = login_page.get_error_message()
            assert test_case["expected_error"] in error_msg

# test_data/login_test_cases.yaml
# - username: "valid@example.com"
#   password: "correct_password"
#   expected_success: true
#   expected_error: ""
# 
# - username: "invalid@example.com"
#   password: "wrong_password"
#   expected_success: false
#   expected_error: "Invalid credentials"
```

## 📊 Reporting Templates

### **Allure интеграция**

```python
# conftest.py
import pytest
import allure
from datetime import datetime

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook для генерации Allure отчетов"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            # Скриншот при падении
            if hasattr(item.funcargs.get('page'), 'screenshot'):
                screenshot = item.funcargs['page'].screenshot()
                allure.attach(
                    screenshot,
                    name=f"screenshot_{datetime.now().strftime('%H-%M-%S')}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

def pytest_configure(config):
    """Конфигурация pytest"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
```

### **HTML отчет**

```python
# reporting/html_reporter.py
import json
from datetime import datetime
from jinja2 import Template

class HTMLReporter:
    """Генератор HTML отчетов"""
    
    def __init__(self):
        self.test_results = []
    
    def add_result(self, test_name: str, status: str, duration: float, 
                   error: str = None, screenshot: str = None):
        """Добавить результат теста"""
        self.test_results.append({
            'name': test_name,
            'status': status,
            'duration': duration,
            'error': error,
            'screenshot': screenshot,
            'timestamp': datetime.now().isoformat()
        })
    
    def generate_report(self, output_path: str):
        """Сгенерировать HTML отчет"""
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Results</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .passed { color: green; }
                .failed { color: red; }
                .table { border-collapse: collapse; width: 100%; }
                .table th, .table td { border: 1px solid #ddd; padding: 8px; }
                .table th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Test Results Report</h1>
            <p>Generated: {{ timestamp }}</p>
            <p>Total tests: {{ total }}, Passed: {{ passed }}, Failed: {{ failed }}</p>
            
            <table class="table">
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration (s)</th>
                    <th>Error</th>
                </tr>
                {% for result in results %}
                <tr>
                    <td>{{ result.name }}</td>
                    <td class="{{ result.status }}">{{ result.status }}</td>
                    <td>{{ "%.2f"|format(result.duration) }}</td>
                    <td>{{ result.error or '' }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """
        
        passed_count = len([r for r in self.test_results if r['status'] == 'PASSED'])
        failed_count = len([r for r in self.test_results if r['status'] == 'FAILED'])
        
        template = Template(template_str)
        html_content = template.render(
            results=self.test_results,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total=len(self.test_results),
            passed=passed_count,
            failed=failed_count
        )
        
        with open(output_path, 'w') as f:
            f.write(html_content)
```

---

## 🎯 Usage Examples

```python
# run_tests.py
#!/usr/bin/env python3
"""
Пример запуска тестов с различными конфигурациями
"""

import subprocess
import sys

def run_smoke_tests():
    """Запустить smoke тесты"""
    cmd = [
        "pytest",
        "tests/",
        "-m", "smoke",
        "--headless",
        "--tb=short",
        "--html=reports/smoke_report.html"
    ]
    return subprocess.run(cmd)

def run_parallel_tests():
    """Запустить параллельные тесты"""
    cmd = [
        "pytest",
        "tests/",
        "-n", "4",  # 4 workers
        "--dist", "loadfile",
        "--reruns", "2",
        "--only-rerun", "AssertionError"
    ]
    return subprocess.run(cmd)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "smoke":
        run_smoke_tests()
    else:
        run_parallel_tests()
```

**Помните:** Эти шаблоны обеспечивают стабильную, поддерживаемую и масштабируемую основу для ваших Playwright тестов!