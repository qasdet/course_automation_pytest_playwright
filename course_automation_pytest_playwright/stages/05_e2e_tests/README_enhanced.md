# 05 — E2E тестирование: сценарии и архитектура

## 🎯 Цели этого этапа

- Освоить создание комплексных end-to-end тестов, имитирующих реальное поведение пользователей
- Научиться проектировать и реализовывать архитектуру тестового фреймворка
- Понять принципы Page Object Model и других паттернов проектирования
- Овладеть техниками организации, параллелизации и отчетности E2E тестов
- Научиться обрабатывать сложные сценарии и flaky тесты

## 📚 Теоретические основы E2E тестирования

### Что такое E2E тестирование?

**End-to-End (E2E) тестирование** - это метод тестирования, который проверяет весь процесс работы приложения от начала до конца, как это делает реальный пользователь.

#### Характеристики E2E тестов:

✅ **Реалистичность** - имитируют настоящее поведение пользователей
✅ **Комплексность** - охватывают всю систему целиком
✅ **Интеграционность** - проверяют взаимодействие всех компонентов
✅ **Бизнес-ориентированность** - фокусируются на пользовательских сценариях

#### Отличия от других типов тестов:

| Аспект | Unit Tests | Integration Tests | E2E Tests |
|--------|------------|-------------------|-----------|
| **Область** | Функция/класс | Модуль/сервис | Вся система |
| **Скорость** | Очень быстрые | Средние | Медленные |
| **Стоимость поддержки** | Низкая | Средняя | Высокая |
| **Стабильность** | Очень стабильные | Средняя | Часто flaky |
| **Покрытие** | Узкое | Среднее | Широкое |

### Архитектура E2E тестов

```
E2E Test Framework
├── Test Runner (pytest)
├── Test Structure
│   ├── tests/                 # Тестовые сценарии
│   ├── pages/                 # Page Objects
│   ├── components/            # Component Objects
│   ├── fixtures/              # Тестовые фикстуры
│   └── utils/                 # Вспомогательные функции
├── Configuration
│   ├── conftest.py           # Глобальные настройки
│   ├── config/               # Конфигурационные файлы
│   └── environments/         # Настройки окружений
└── Reporting
    ├── reports/              # Отчеты и логи
    ├── screenshots/          # Скриншоты
    └── videos/               # Видеозаписи тестов
```

### Паттерны проектирования для E2E тестов

#### 1. Page Object Model (POM)
- Инкапсуляция логики работы со страницами
- Повышение переиспользуемости кода
- Упрощение поддержки тестов

#### 2. Component Object Model
- Разбиение страниц на компоненты
- Повышение модульности
- Упрощение сложных интерфейсов

#### 3. Data Builder Pattern
- Создание тестовых данных
- Повышение читаемости тестов
- Упрощение настройки тестовых сценариев

#### 4. Factory Pattern
- Создание page/component объектов
- Централизованное управление
- Гибкость в создании объектов

## 🛠️ Подробное руководство по E2E тестированию

### Структура проекта

```
e2e_project/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_user_flows.py
│   ├── test_authentication.py
│   └── test_checkout_process.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── product_page.py
├── components/
│   ├── __init__.py
│   ├── navigation_menu.py
│   ├── search_bar.py
│   └── cart_widget.py
├── fixtures/
│   ├── __init__.py
│   ├── user_fixtures.py
│   └── data_fixtures.py
├── utils/
│   ├── __init__.py
│   ├── test_data_builder.py
│   ├── wait_helpers.py
│   └── screenshot_helper.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── environments.py
├── reports/
│   ├── html_reports/
│   ├── xml_reports/
│   └── screenshots/
└── requirements.txt
```

### Базовая реализация Page Object

```python
# pages/base_page.py
from playwright.sync_api import Page, Locator
from typing import Optional


class BasePage:
    """Базовый класс для всех page objects"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000
    
    def navigate_to(self, url: str) -> None:
        """Навигация к URL"""
        self.page.goto(url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self) -> None:
        """Ожидание загрузки страницы"""
        self.page.wait_for_load_state("networkidle")
    
    def get_element(self, selector: str) -> Locator:
        """Получение элемента с базовым таймаутом"""
        return self.page.locator(selector).first
    
    def click_element(self, selector: str) -> None:
        """Клик по элементу с ожиданием"""
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=self.timeout)
        element.click()
    
    def fill_field(self, selector: str, value: str) -> None:
        """Заполнение поля ввода"""
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=self.timeout)
        element.fill(value)
    
    def get_text(self, selector: str) -> str:
        """Получение текста элемента"""
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=self.timeout)
        return element.text_content() or ""
    
    def is_element_visible(self, selector: str) -> bool:
        """Проверка видимости элемента"""
        try:
            element = self.get_element(selector)
            return element.is_visible()
        except:
            return False


# pages/login_page.py
from pages.base_page import BasePage
from typing import Optional


class LoginPage(BasePage):
    """Page Object для страницы логина"""
    
    # Локаторы
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    SUCCESS_REDIRECT = ".dashboard"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://example.com/login"
    
    def load(self) -> None:
        """Загрузка страницы логина"""
        self.navigate_to(self.url)
    
    def login(self, username: str, password: str) -> None:
        """Выполнение логина"""
        self.fill_field(self.USERNAME_INPUT, username)
        self.fill_field(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> Optional[str]:
        """Получение сообщения об ошибке"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_logged_in(self) -> bool:
        """Проверка успешного логина"""
        return self.is_element_visible(self.SUCCESS_REDIRECT)
```

### Реализация тестов с Page Objects

```python
# tests/test_authentication.py
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestAuthentication:
    """Тесты аутентификации"""
    
    def test_successful_login(self, page):
        """Тест успешного логина"""
        # ARRANGE
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # ACT
        login_page.load()
        login_page.login("valid_user", "valid_password")
        
        # ASSERT
        assert dashboard_page.is_loaded()
        assert dashboard_page.get_username() == "valid_user"
    
    def test_invalid_credentials(self, page):
        """Тест неверных учетных данных"""
        # ARRANGE
        login_page = LoginPage(page)
        
        # ACT
        login_page.load()
        login_page.login("invalid_user", "wrong_password")
        
        # ASSERT
        error_message = login_page.get_error_message()
        assert error_message is not None
        assert "Invalid credentials" in error_message
        assert not login_page.is_logged_in()
    
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "password", "Username is required"),
        ("user", "", "Password is required"),
        ("", "", "Username is required"),
    ])
    def test_required_fields(self, page, username, password, expected_error):
        """Тест обязательных полей"""
        # ARRANGE
        login_page = LoginPage(page)
        
        # ACT
        login_page.load()
        login_page.login(username, password)
        
        # ASSERT
        error_message = login_page.get_error_message()
        assert error_message is not None
        assert expected_error in error_message
```

### Component Object Pattern

```python
# components/navigation_menu.py
from playwright.sync_api import Page, Locator


class NavigationMenu:
    """Component Object для навигационного меню"""
    
    MENU_TOGGLE = ".menu-toggle"
    MENU_ITEMS = ".menu-item"
    ACTIVE_ITEM = ".menu-item.active"
    
    def __init__(self, page: Page):
        self.page = page
    
    def open_menu(self) -> None:
        """Открытие меню"""
        self.page.locator(self.MENU_TOGGLE).click()
    
    def click_menu_item(self, item_text: str) -> None:
        """Клик по пункту меню"""
        menu_items = self.page.locator(self.MENU_ITEMS)
        menu_items.filter(has_text=item_text).click()
    
    def get_active_item(self) -> str:
        """Получение активного пункта меню"""
        return self.page.locator(self.ACTIVE_ITEM).text_content() or ""


# pages/dashboard_page.py
from pages.base_page import BasePage
from components.navigation_menu import NavigationMenu


class DashboardPage(BasePage):
    """Page Object для дашборда"""
    
    USERNAME_DISPLAY = ".user-name"
    LOGOUT_BUTTON = ".logout-btn"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.navigation = NavigationMenu(page)
    
    def is_loaded(self) -> bool:
        """Проверка загрузки страницы"""
        return self.is_element_visible(self.USERNAME_DISPLAY)
    
    def get_username(self) -> str:
        """Получение имени пользователя"""
        return self.get_text(self.USERNAME_DISPLAY)
    
    def logout(self) -> None:
        """Выход из системы"""
        self.click_element(self.LOGOUT_BUTTON)
```

## 🔄 Организация тестовых данных

### Data Builder Pattern

```python
# utils/test_data_builder.py
from dataclasses import dataclass
from typing import Optional
import random
import string


@dataclass
class UserData:
    """Модель пользовательских данных"""
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class TestDataBuilder:
    """Builder для создания тестовых данных"""
    
    @staticmethod
    def random_string(length: int = 8) -> str:
        """Генерация случайной строки"""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @staticmethod
    def random_email() -> str:
        """Генерация случайного email"""
        return f"{TestDataBuilder.random_string()}@test.com"
    
    @classmethod
    def valid_user(cls) -> UserData:
        """Создание валидного пользователя"""
        return UserData(
            username=cls.random_string(),
            email=cls.random_email(),
            password="SecurePass123!",
            first_name="John",
            last_name="Doe"
        )
    
    @classmethod
    def invalid_user(cls) -> UserData:
        """Создание невалидного пользователя"""
        return UserData(
            username="",
            email="invalid-email",
            password="123",
            first_name="",
            last_name=""
        )


# Использование в тестах
def test_user_registration(page):
    """Тест регистрации пользователя"""
    user_data = TestDataBuilder.valid_user()
    
    registration_page = RegistrationPage(page)
    registration_page.register(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    
    # Проверки...
```

## 📊 Параллелизация и отчетность

### Настройка параллельного запуска

```bash
# Установка необходимых пакетов
pip install pytest-xdist pytest-html

# Параллельный запуск
pytest -n 4  # 4 процесса
pytest -n auto  # Автоматическое определение количества процессов

# Запуск с группировкой по классам
pytest -n auto --dist=loadscope

# Запуск с распределением по файлам
pytest -n auto --dist=loadfile
```

### Конфигурация отчетности

```python
# conftest.py - Расширенная конфигурация
import pytest
import os
from datetime import datetime


@pytest.fixture(scope="session")
def test_results_dir():
    """Фикстура для директории результатов"""
    results_dir = "test_results"
    os.makedirs(results_dir, exist_ok=True)
    return results_dir


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page, test_results_dir):
    """Автоматические скриншоты при ошибках"""
    yield
    
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = os.path.join(
            test_results_dir, 
            f"failure_{test_name}_{timestamp}.png"
        )
        page.screenshot(path=screenshot_path, full_page=True)


def pytest_html_report_title(report):
    """Заголовок HTML отчета"""
    report.title = "E2E Test Report"


def pytest_configure(config):
    """Конфигурация pytest"""
    config.option.htmlpath = "reports/report.html"
    config.option.self_contained_html = True
```

### Команды для генерации отчетов

```bash
# HTML отчет
pytest --html=reports/report.html --self-contained-html

# JUnit XML для CI/CD
pytest --junitxml=reports/results.xml

# Покрытие кода (если применимо)
pytest --cov=pages --cov-report=html:reports/coverage

# Все отчеты сразу
pytest -n auto \
    --html=reports/report.html \
    --self-contained-html \
    --junitxml=reports/results.xml \
    --cov=pages \
    --cov-report=html:reports/coverage
```

## 🤔 Часто задаваемые вопросы (FAQ)

### **Q: Как бороться с flaky E2E тестами?**
**A:** 
- Используйте стабильные селекторы
- Добавьте правильные ожидания
- Изолируйте тестовые данные
- Используйте retry mechanisms
- Добавьте логирование для диагностики

### **Q: Сколько E2E тестов нужно писать?**
**A:** Следуйте тестовой пирамиде: 70% unit, 20% integration, 10% E2E. Фокусируйтесь на критических пользовательских сценариях.

### **Q: Как организовать тестовые данные?**
**A:** Используйте data builders, фикстуры и отделяйте тестовые данные от тестовой логики.

### **Q: Когда использовать Page Object, а когда Component Object?**
**A:** Page Object для целых страниц, Component Object для повторяющихся UI компонентов (меню, формы, виджеты).

## ✅ Чеклист E2E тестирования

### Архитектура
- [ ] Использую Page Object Model для страниц
- [ ] Применяю Component Object для UI компонентов
- [ ] Создаю базовые классы для переиспользования
- [ ] Организую четкую структуру проекта

### Тестовые данные
- [ ] Использую data builders для генерации данных
- [ ] Изолирую тестовые данные от production
- [ ] Создаю фикстуры для повторяющихся данных
- [ ] Обеспечиваю уникальность тестовых данных

### Стабильность
- [ ] Использую стабильные селекторы
- [ ] Добавляю правильные ожидания
- [ ] Обрабатываю динамический контент
- [ ] Добавляю retry mechanisms для flaky тестов

### Производительность
- [ ] Настраиваю параллельный запуск
- [ ] Оптимизирую использование ресурсов
- [ ] Использую session-scoped фикстуры
- [ ] Минимизирую время setup/teardown

### Отчетность
- [ ] Настраиваю HTML отчеты
- [ ] Добавляю скриншоты при ошибках
- [ ] Генерирую JUnit XML для CI/CD
- [ ] Настраиваю логирование

## 💡 Практическое задание

### Часть 1: Архитектура
1. Создайте структуру проекта с Page Objects
2. Реализуйте базовый класс для страниц
3. Создайте несколько page objects для демо сайта

### Часть 2: Тестовые сценарии
1. Напишите E2E тесты для пользовательских сценариев
2. Используйте data builders для тестовых данных
3. Добавьте component objects для повторяющихся элементов

### Часть 3: Производительность и отчетность
1. Настройте параллельный запуск тестов
2. Реализуйте автоматические скриншоты при ошибках
3. Сгенерируйте HTML и XML отчеты

## ⚠️ Распространенные ошибки и решения

| Ошибка | Причина | Решение |
|--------|---------|---------|
| "Element not found" | Хрупкие селекторы | Используйте стабильные атрибуты (data-testid) |
| "Timeout waiting for element" | Неправильные ожидания | Добавьте явные ожидания или увеличьте таймауты |
| "Tests interfering with each other" | Нет изоляции | Используйте отдельные browser contexts |
| "Flaky tests" | Динамический контент | Добавьте правильные wait conditions |

## 📚 Полезные ресурсы

### Паттерны и практики:
- **Page Object Model** - стандартный паттерн для UI тестов
- **Component Object Model** - для повторяющихся UI компонентов
- **Factory Pattern** - для создания тестовых объектов
- **Data Builder Pattern** - для генерации тестовых данных

### Инструменты:
- **pytest-xdist** - параллельный запуск тестов
- **pytest-html** - HTML отчеты
- **allure-pytest** - продвинутая отчетность
- **playwright-trace** - трассировка выполнения тестов

### Best Practices:
- Следуйте тестовой пирамиде
- Делайте тесты независимыми
- Используйте осмысленные имена
- Поддерживайте тесты в актуальном состоянии
- Добавляйте диагностику для flaky тестов