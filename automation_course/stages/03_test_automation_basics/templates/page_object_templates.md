# 📋 Шаблоны Page Object

## 🎯 Основные принципы Page Object Model

### **Что такое Page Object?**
Page Object - это паттерн проектирования, который создает объектную модель пользовательского интерфейса приложения. Каждая страница представлена как класс, содержащий элементы страницы и методы для взаимодействия с ними.

### **Преимущества POM:**
✅ **Поддерживаемость** - изменения в UI требуют правки только в одном месте
✅ **Переиспользуемость** - методы можно использовать в разных тестах
✅ **Читаемость** - тесты становятся более понятными
✅ **Стабильность** - меньше flaky тестов

## 🏗️ Базовые шаблоны

### **Базовый Page Object**

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
    
    def find_element(self, locator):
        """Найти элемент с ожиданием"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """Найти все элементы"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator):
        """Кликнуть по элементу"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return self
    
    def send_keys(self, locator, text):
        """Ввести текст в поле"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return self
    
    def get_text(self, locator):
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text
    
    def is_displayed(self, locator):
        """Проверить, отображается ли элемент"""
        try:
            element = self.find_element(locator)
            return element.is_displayed()
        except:
            return False
    
    def wait_for_element_visible(self, locator):
        """Ждать появления элемента"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_invisible(self, locator):
        """Ждать исчезновения элемента"""
        return self.wait.until(EC.invisibility_of_element_located(locator))
    
    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url
    
    def get_title(self):
        """Получить заголовок страницы"""
        return self.driver.title
```

### **Пример конкретной страницы**

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    """Page Object для страницы логина"""
    
    # Локаторы элементов
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot password?")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com/login"
    
    def navigate(self):
        """Перейти на страницу логина"""
        self.driver.get(self.url)
        return self
    
    def enter_username(self, username):
        """Ввести имя пользователя"""
        self.send_keys(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password):
        """Ввести пароль"""
        self.send_keys(self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self):
        """Нажать кнопку логина"""
        self.click(self.LOGIN_BUTTON)
        return DashboardPage(self.driver)  # Возвращаем следующую страницу
    
    def login(self, username, password):
        """Полный процесс логина"""
        return (self
                .enter_username(username)
                .enter_password(password)
                .click_login())
    
    def get_error_message(self):
        """Получить сообщение об ошибке"""
        if self.is_displayed(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def click_forgot_password(self):
        """Нажать ссылку восстановления пароля"""
        self.click(self.FORGOT_PASSWORD_LINK)
        return ForgotPasswordPage(self.driver)
    
    def toggle_remember_me(self):
        """Переключить чекбокс запомнить меня"""
        self.click(self.REMEMBER_ME_CHECKBOX)
        return self
    
    def is_login_button_enabled(self):
        """Проверить, активна ли кнопка логина"""
        button = self.find_element(self.LOGIN_BUTTON)
        return button.is_enabled()
```

## 🎨 Шаблоны для разных типов страниц

### **Dashboard Page**

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class DashboardPage(BasePage):
    """Page Object для дашборда"""
    
    # Локаторы
    USER_MENU = (By.ID, "user-menu")
    LOGOUT_BUTTON = (By.ID, "logout-btn")
    NOTIFICATIONS_BADGE = (By.CLASS_NAME, "notifications-count")
    WELCOME_MESSAGE = (By.XPATH, "//h1[contains(text(), 'Welcome')]")
    PROJECT_LIST = (By.CLASS_NAME, "project-list")
    CREATE_PROJECT_BUTTON = (By.ID, "create-project-btn")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com/dashboard"
    
    def is_loaded(self):
        """Проверить, загрузилась ли страница"""
        return self.is_displayed(self.WELCOME_MESSAGE)
    
    def get_notifications_count(self):
        """Получить количество уведомлений"""
        if self.is_displayed(self.NOTIFICATIONS_BADGE):
            return int(self.get_text(self.NOTIFICATIONS_BADGE))
        return 0
    
    def open_user_menu(self):
        """Открыть пользовательское меню"""
        self.click(self.USER_MENU)
        return self
    
    def logout(self):
        """Выполнить выход"""
        self.open_user_menu()
        self.click(self.LOGOUT_BUTTON)
        return LoginPage(self.driver)
    
    def get_projects_list(self):
        """Получить список проектов"""
        projects = self.find_elements(self.PROJECT_LIST)
        return [project.text for project in projects]
    
    def click_create_project(self):
        """Нажать кнопку создания проекта"""
        self.click(self.CREATE_PROJECT_BUTTON)
        return CreateProjectPage(self.driver)
```

### **Form Page**

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage

class RegistrationPage(BasePage):
    """Page Object для страницы регистрации"""
    
    # Локаторы
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirm-password")
    BIRTH_DATE_INPUT = (By.ID, "birth-date")
    GENDER_SELECT = (By.ID, "gender")
    TERMS_CHECKBOX = (By.ID, "terms-agreement")
    SUBMIT_BUTTON = (By.ID, "submit-registration")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    
    def fill_personal_info(self, first_name, last_name, email):
        """Заполнить персональную информацию"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        return self
    
    def enter_first_name(self, name):
        self.send_keys(self.FIRST_NAME_INPUT, name)
        return self
    
    def enter_last_name(self, name):
        self.send_keys(self.LAST_NAME_INPUT, name)
        return self
    
    def enter_email(self, email):
        self.send_keys(self.EMAIL_INPUT, email)
        return self
    
    def enter_phone(self, phone):
        self.send_keys(self.PHONE_INPUT, phone)
        return self
    
    def enter_password(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)
        return self
    
    def confirm_password(self, password):
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, password)
        return self
    
    def select_birth_date(self, date):
        self.send_keys(self.BIRTH_DATE_INPUT, date)
        return self
    
    def select_gender(self, gender):
        """Выбрать пол из dropdown"""
        select = Select(self.find_element(self.GENDER_SELECT))
        select.select_by_visible_text(gender)
        return self
    
    def accept_terms(self):
        """Принять условия"""
        if not self.find_element(self.TERMS_CHECKBOX).is_selected():
            self.click(self.TERMS_CHECKBOX)
        return self
    
    def submit_form(self):
        """Отправить форму"""
        self.click(self.SUBMIT_BUTTON)
        return self
    
    def register_user(self, user_data):
        """Полная регистрация пользователя"""
        return (self
                .fill_personal_info(
                    user_data['first_name'],
                    user_data['last_name'], 
                    user_data['email']
                )
                .enter_phone(user_data['phone'])
                .enter_password(user_data['password'])
                .confirm_password(user_data['password'])
                .select_birth_date(user_data['birth_date'])
                .select_gender(user_data['gender'])
                .accept_terms()
                .submit_form())
    
    def is_success_message_displayed(self):
        """Проверить успешную регистрацию"""
        return self.is_displayed(self.SUCCESS_MESSAGE)
```

## 🛠️ Компонентные Page Objects

### **Header Component**

```python
from selenium.webdriver.common.by import By
from .base_component import BaseComponent

class Header(BaseComponent):
    """Компонент хедера сайта"""
    
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.ID, "search-button")
    CART_ICON = (By.ID, "cart-icon")
    CART_COUNT = (By.CLASS_NAME, "cart-count")
    USER_AVATAR = (By.CLASS_NAME, "user-avatar")
    NOTIFICATIONS_ICON = (By.ID, "notifications")
    
    def search_for(self, query):
        """Поиск по сайту"""
        self.send_keys(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        return SearchResultsPage(self.driver)
    
    def get_cart_items_count(self):
        """Получить количество товаров в корзине"""
        if self.is_displayed(self.CART_COUNT):
            return int(self.get_text(self.CART_COUNT))
        return 0
    
    def open_cart(self):
        """Открыть корзину"""
        self.click(self.CART_ICON)
        return CartPage(self.driver)
    
    def open_user_profile(self):
        """Открыть профиль пользователя"""
        self.click(self.USER_AVATAR)
        return ProfilePage(self.driver)
```

### **Modal Window Component**

```python
from selenium.webdriver.common.by import By
from .base_component import BaseComponent

class ConfirmationModal(BaseComponent):
    """Компонент модального окна подтверждения"""
    
    MODAL_CONTAINER = (By.CLASS_NAME, "modal-container")
    TITLE = (By.CLASS_NAME, "modal-title")
    MESSAGE = (By.CLASS_NAME, "modal-message")
    CONFIRM_BUTTON = (By.ID, "confirm-btn")
    CANCEL_BUTTON = (By.ID, "cancel-btn")
    CLOSE_BUTTON = (By.CLASS_NAME, "modal-close")
    
    def is_displayed(self):
        """Проверить, отображается ли модальное окно"""
        return self.is_element_present(self.MODAL_CONTAINER)
    
    def get_title(self):
        """Получить заголовок модального окна"""
        return self.get_text(self.TITLE)
    
    def get_message(self):
        """Получить сообщение модального окна"""
        return self.get_text(self.MESSAGE)
    
    def confirm(self):
        """Подтвердить действие"""
        self.click(self.CONFIRM_BUTTON)
        return self
    
    def cancel(self):
        """Отменить действие"""
        self.click(self.CANCEL_BUTTON)
        return self
    
    def close(self):
        """Закрыть модальное окно"""
        self.click(self.CLOSE_BUTTON)
        return self
```

## 🎯 Advanced Patterns

### **Factory Pattern для Page Objects**

```python
from enum import Enum
from .pages import LoginPage, DashboardPage, RegistrationPage

class PageType(Enum):
    LOGIN = "login"
    DASHBOARD = "dashboard"
    REGISTRATION = "registration"

class PageFactory:
    """Фабрика для создания Page Objects"""
    
    @staticmethod
    def create_page(driver, page_type):
        """Создать страницу по типу"""
        pages = {
            PageType.LOGIN: LoginPage,
            PageType.DASHBOARD: DashboardPage,
            PageType.REGISTRATION: RegistrationPage
        }
        
        if page_type not in pages:
            raise ValueError(f"Unknown page type: {page_type}")
        
        return pages[page_type](driver)
    
    @staticmethod
    def create_pages_dict(driver):
        """Создать словарь всех страниц"""
        return {
            'login': LoginPage(driver),
            'dashboard': DashboardPage(driver),
            'registration': RegistrationPage(driver)
        }
```

### **Page Object с Fluent Interface**

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProductPage(BasePage):
    """Page Object с fluent interface"""
    
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart")
    QUANTITY_INPUT = (By.ID, "quantity")
    PRODUCT_TITLE = (By.CLASS_NAME, "product-title")
    PRODUCT_PRICE = (By.CLASS_NAME, "product-price")
    WISHLIST_BUTTON = (By.ID, "wishlist-btn")
    
    def with_quantity(self, quantity):
        """Установить количество (fluent)"""
        self.send_keys(self.QUANTITY_INPUT, str(quantity))
        return self
    
    def add_to_cart(self):
        """Добавить в корзину (fluent)"""
        self.click(self.ADD_TO_CART_BUTTON)
        return CartPage(self.driver)
    
    def add_to_wishlist(self):
        """Добавить в wishlist (fluent)"""
        self.click(self.WISHLIST_BUTTON)
        return self
    
    def get_product_info(self):
        """Получить информацию о продукте"""
        return {
            'title': self.get_text(self.PRODUCT_TITLE),
            'price': self.get_text(self.PRODUCT_PRICE)
        }
    
    # Использование:
    # product_page.with_quantity(3).add_to_cart()
```

## 📋 Best Practices

### **Naming Conventions**

```python
# ✅ Хорошо
class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    LOGIN_BUTTON = (By.ID, "login-btn")
    
    def enter_username(self, username):
        pass
    
    def click_login_button(self):
        pass

# ❌ Плохо
class loginPage:
    userField = (By.ID, "user")
    btn = (By.ID, "button")
    
    def inputUser(self, user):
        pass
```

### **Error Handling**

```python
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class RobustPage(BasePage):
    """Page Object с обработкой ошибок"""
    
    def safe_click(self, locator, timeout=5):
        """Безопасный клик с обработкой исключений"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Element not clickable: {locator}")
            return False
    
    def wait_for_page_load(self, timeout=10):
        """Ждать полной загрузки страницы"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            print("Page failed to load within timeout")
            return False
```

### **Configuration Management**

```python
import os
from dataclasses import dataclass

@dataclass
class PageConfig:
    """Конфигурация для Page Objects"""
    base_url: str
    timeout: int = 10
    implicit_wait: int = 5
    page_load_timeout: int = 30

class ConfigurablePage(BasePage):
    """Page Object с поддержкой конфигурации"""
    
    def __init__(self, driver, config: PageConfig):
        super().__init__(driver, config.timeout)
        self.config = config
        self.driver.implicitly_wait(config.implicit_wait)
        self.driver.set_page_load_timeout(config.page_load_timeout)
    
    def get_full_url(self, path):
        """Получить полный URL"""
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"
```

## 🎯 Пример использования

```python
# conftest.py
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def dashboard_page(driver):
    return DashboardPage(driver)

# test_example.py
def test_user_login(login_page, dashboard_page):
    # Arrange
    username = "testuser@example.com"
    password = "password123"
    
    # Act
    login_page.navigate()
    dashboard = login_page.login(username, password)
    
    # Assert
    assert dashboard.is_loaded()
    assert "dashboard" in dashboard.get_current_url()
```

---

## 📝 Советы по применению

1. **Начинайте с простого** - не усложняйте сразу
2. **Следуйте Single Responsibility Principle** - один класс = одна страница
3. **Используйте описательные имена** - методы должны читаться как предложения
4. **Не храните состояние** - Page Objects должны быть stateless
5. **Обрабатывайте исключения** - делайте тесты устойчивыми
6. **Документируйте** - добавляйте docstrings к методам
7. **Тестируйте Page Objects** - unit тесты для page object классов

**Помните:** Хорошо спроектированные Page Objects - залог стабильной и поддерживаемой автоматизации!