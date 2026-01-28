# Модуль 4: Playwright - Основы

## 🎯 Цели модуля (4 недели / 16 занятий)

**По окончании модуля студент сможет:**
- Глубоко понимать архитектуру Playwright
- Эффективно работать с локаторами и селекторами
- Применять Page Object Pattern в тестировании
- Создавать надежные и поддерживаемые UI тесты
- Обрабатывать сложные сценарии взаимодействия с веб-приложениями
- **Строить масштабируемые тестовые фреймворки**
- **Реализовывать best practices UI автоматизации**
- **Настраивать параллельное выполнение тестов**

## 👨‍🏫 Методические материалы для преподавателя

### Общие рекомендации по преподаванию Playwright:

**🎯 Основной подход:**
- **Постепенное усложнение:** От простых действий к сложным сценариям
- **Практическая направленность:** Каждая концепция закрепляется кодом
- **Реальные примеры:** Использовать production-подобные приложения
- **Debugging навыки:** Учить студентов отладке тестов
- **Best practices:** Постоянно демонстрировать правильные подходы

**📋 Необходимые ресурсы:**
- Тестовые стенды с разными типами веб-приложений
- Примеры с преднамеренными багами
- Production-like applications для realistic testing
- Инструменты мониторинга и отладки
- **Шаблоны Page Object классов**

**⏰ Структура занятий:**
- 10 мин: Проверка домашнего задания
- 20 мин: Теория и демонстрации
- 35 мин: Live coding и практика
- 15 мин: Перерыв
- 25 мин: Самостоятельная работа
- 15 мин: Подведение итогов

## 📚 Архитектура Playwright

### Понимание архитектуры

```python
# АРХИТЕКТУРА PLAYWRIGHT - КОМПОНЕНТЫ И ВЗАИМОДЕЙСТВИЕ

class PlaywrightArchitecture:
    def __init__(self):
        self.components = {}
        self.communication_patterns = {}
    
    def core_components(self):
        """
        Основные компоненты Playwright
        """
        return {
            "Browser": {
                "description": "Управляет браузерными процессами",
                "types": ["chromium", "firefox", "webkit"],
                "responsibilities": [
                    "Запуск/остановка браузера",
                    "Управление контекстами",
                    "Настройка параметров браузера"
                ]
            },
            
            "BrowserContext": {
                "description": "Изолированная среда браузера",
                "features": [
                    "Cookies изоляция",
                    "Storage изоляция", 
                    "Proxy настройки",
                    "Geolocation mocking"
                ]
            },
            
            "Page": {
                "description": "Представление вкладки браузера",
                "capabilities": [
                    "Навигация по страницам",
                    "Взаимодействие с DOM",
                    "Работа с frames",
                    "Network interception"
                ]
            },
            
            "Locator": {
                "description": "Интеллектуальные селекторы",
                "advantages": [
                    "Auto-waiting механизм",
                    "Retry-ability",
                    "Stable selectors",
                    "Chainable operations"
                ]
            }
        }
    
    def communication_flow(self):
        """
        Поток взаимодействия компонентов
        """
        flow = """
        Test Script
            ↓
        Playwright (Python bindings)
            ↓
        Playwright Driver (Node.js)
            ↓
        Browser Process
            ↓
        Browser Context
            ↓
        Page/Frame
            ↓
        DOM Elements
        """
        return flow

# ПРАКТИЧЕСКАЯ РЕАЛИЗАЦИЯ АРХИТЕКТУРЫ

class PracticalPlaywrightSetup:
    def basic_browser_management(self):
        """Базовое управление браузером"""
        
        from playwright.sync_api import sync_playwright
        
        def run_test_with_context():
            with sync_playwright() as p:
                # Запуск браузера
                browser = p.chromium.launch(
                    headless=False,  # Видимый режим для отладки
                    slow_mo=1000     # Замедление для наблюдения
                )
                
                # Создание контекста
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    locale="ru-RU",
                    timezone_id="Europe/Moscow"
                )
                
                # Создание страницы
                page = context.new_page()
                
                try:
                    # Тестовая логика
                    page.goto("https://example.com")
                    assert "Example" in page.title()
                    
                finally:
                    # Очистка
                    context.close()
                    browser.close()
        
        return run_test_with_context
    
    def advanced_context_configuration(self):
        """Продвинутая настройка контекста"""
        
        def configure_test_context(playwright):
            return playwright.chromium.launchPersistentContext(
                "./user-data-dir",  # Сохранение сессии
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ],
                viewport={"width": 1920, "height": 1080},
                device_scale_factor=1,
                is_mobile=False,
                has_touch=False,
                java_script_enabled=True,
                accept_downloads=True,
                downloads_path="./downloads",
                bypass_csp=True,  # Обход Content Security Policy
                ignore_https_errors=True
            )
        
        return configure_test_context

# ЛУЧШИЕ ПРАКТИКИ ДЛЯ АРХИТЕКТУРЫ:
architecture_best_practices = [
    "Используйте контексты для изоляции тестов",
    "Закрывайте ресурсы в блоках finally",
    "Конфигурируйте браузер через параметры запуска",
    "Используйте persistent context для сессий",
    "Применяйте правильные viewport размеры"
]
```

### Сравнение с другими инструментами

```python
# СРАВНЕНИЕ PLAYWRIGHT С ДРУГИМИ ИНСТРУМЕНТАМИ

class ToolComparison:
    def __init__(self):
        self.comparison_matrix = {}
    
    def detailed_comparison(self):
        """
        Подробное сравнение инструментов автоматизации
        """
        comparison = {
            "Playwright": {
                "pros": [
                    "Авто-ожидание элементов",
                    "Встроенный retry mechanism",
                    "Поддержка всех современных браузеров",
                    "Мощные локаторы",
                    "Хорошая документация",
                    "Активное сообщество"
                ],
                "cons": [
                    "Относительно новый (меньше legacy знаний)",
                    "Требует Node.js для драйвера"
                ],
                "best_for": [
                    "Современные веб-приложения",
                    "Cross-browser тестирование",
                    "Комплексная автоматизация"
                ]
            },
            
            "Selenium": {
                "pros": [
                    "Зрелая экосистема",
                    "Много языковых биндингов",
                    "Большое сообщество",
                    "Широкая поддержка"
                ],
                "cons": [
                    "Требует явных ожиданий",
                    "Медленнее чем Playwright",
                    "Более хрупкие тесты",
                    "Сложная настройка grid"
                ],
                "best_for": [
                    "Legacy приложения",
                    "Когда нужна Java/C# поддержка",
                    "Enterprise среды"
                ]
            },
            
            "Cypress": {
                "pros": [
                    "Отличная DX (Developer Experience)",
                    "Встроенный тест runner",
                    "Real-time reloads",
                    "Хорош для frontend разработчиков"
                ],
                "cons": [
                    "Только Chrome/Firefox",
                    "Ограниченная поддержка tabs/iframes",
                    "Не подходит для complex flows"
                ],
                "best_for": [
                    "Frontend unit/e2e тесты",
                    "React/Vue приложения",
                    "Разработчики как тестировщики"
                ]
            }
        }
        
        return comparison
    
    def why_playwright_for_this_course(self):
        """
        Почему Playwright выбран для этого курса
        """
        return {
            "modern_web_support": "Лучшая поддержка современных веб-технологий",
            "reliability": "Встроенные механизмы стабильности тестов",
            "ease_of_learning": "Интуитивный API для новичков",
            "comprehensive": "Один инструмент для всех нужд автоматизации",
            "performance": "Быстрое выполнение тестов",
            "future_ready": "Активная разработка и поддержка"
        }

# ПРАКТИЧЕСКИЕ ПРИМЕРЫ СРАВНЕНИЯ:

class PracticalComparisons:
    def playwright_vs_selenium_example(self):
        """Сравнение одного и того же теста"""
        
        # PLAYWRIGHT VERSION
        def playwright_login_test(page):
            page.goto("https://example.com/login")
            page.fill("#username", "user")
            page.fill("#password", "pass")
            page.click("#login-btn")
            # Автоматическое ожидание загрузки страницы
            assert page.url == "https://example.com/dashboard"
        
        # SELENIUM VERSION
        def selenium_login_test(driver):
            driver.get("https://example.com/login")
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username.send_keys("user")
            
            password = driver.find_element(By.ID, "password")
            password.send_keys("pass")
            
            login_btn = driver.find_element(By.ID, "login-btn")
            login_btn.click()
            
            WebDriverWait(driver, 10).until(
                EC.url_contains("dashboard")
            )
            assert "dashboard" in driver.current_url
        
        return {
            "playwright_lines": 6,
            "selenium_lines": 15,
            "playwright_wait": "Автоматическое",
            "selenium_wait": "Явное ожидание",
            "readability": "Playwright более читаем"
        }
```

## 🎯 Локаторы и селекторы

### Мастерство работы с локаторами

```python
# ПОЛНОЕ РУКОВОДСТВО ПО ЛОКАТОРАМ

class LocatorMastery:
    def __init__(self):
        self.locator_types = {}
        self.best_practices = []
    
    def css_selectors_comprehensive(self, page):
        """Полное руководство по CSS селекторам"""
        
        # БАЗОВЫЕ СЕЛЕКТОРЫ
        examples = {
            # По ID
            "by_id": page.locator("#submit-button"),
            
            # По классу
            "by_class": page.locator(".btn-primary"),
            
            # По атрибуту
            "by_attribute": page.locator("[data-testid='login-form']"),
            
            # По имени
            "by_name": page.locator("[name='username']"),
            
            # По типу
            "by_type": page.locator("input[type='email']"),
            
            # По тексту (точное совпадение)
            "by_exact_text": page.locator("text=Войти"),
            
            # По тексту (частичное совпадение)
            "by_partial_text": page.locator("text=Вой"),
            
            # Комбинированные
            "combined": page.locator("form.login-form input.required[type='password']")
        }
        
        # СЛОЖНЫЕ СЕЛЕКТОРЫ
        advanced_examples = {
            # Псевдоклассы
            "first_child": page.locator("li:first-child"),
            "last_child": page.locator("li:last-child"),
            "nth_child": page.locator("tr:nth-child(2)"),
            "even_elements": page.locator("tr:nth-child(even)"),
            
            # Отношения
            "descendant": page.locator("form .input-field"),  # Потомок
            "child": page.locator("ul > li"),                 # Прямой потомок
            "adjacent_sibling": page.locator("h1 + p"),       # Следующий сосед
            "general_sibling": page.locator("h1 ~ p"),        # Все следующие соседи
            
            # Атрибуты с условиями
            "attribute_contains": page.locator("[class*='btn']"),      # Содержит
            "attribute_starts": page.locator("[href^='https']"),       # Начинается с
            "attribute_ends": page.locator("[src$='.png']"),           # Заканчивается на
            "attribute_not_equal": page.locator("[class!='disabled']")  # Не равно
        }
        
        return {**examples, **advanced_examples}
    
    def xpath_selectors_guide(self, page):
        """Руководство по XPath (когда CSS недостаточно)"""
        
        xpath_examples = {
            # Навигация по дереву
            "absolute_path": page.locator("/html/body/div/form/input[1]"),
            "relative_path": page.locator("//input[@name='username']"),
            
            # По тексту
            "exact_text": page.locator("//button[text()='Submit']"),
            "contains_text": page.locator("//div[contains(text(), 'Welcome')]"),
            "normalize_space": page.locator("//span[normalize-space()='Log In']"),
            
            # По индексу
            "by_position": page.locator("(//li)[3]"),  # Третий элемент списка
            "last_element": page.locator("(//option)[last()]"),
            
            # Оси XPath
            "parent_axis": page.locator("//input[@name='email']/.."),           # Родитель
            "following_sibling": page.locator("//h1/following-sibling::p"),     # Следующий сосед
            "preceding_sibling": page.locator("//p/preceding-sibling::h1"),     # Предыдущий сосед
            "ancestor": page.locator("//input[@id='search']/ancestor::form"),   # Предок
            "descendant": page.locator("//div[@class='container']//input")      # Потомок
        }
        
        return xpath_examples
    
    def advanced_locator_techniques(self, page):
        """Продвинутые техники локаторов"""
        
        # CHAIN LOCATORS
        chain_examples = {
            "nested_search": page.locator(".modal").locator(".close-button"),
            "filter_chain": page.locator("button").filter(has_text="Delete"),
            "multiple_filters": page.locator("div")
                .filter(has=page.locator(".header"))
                .filter(has_text="Important")
        }
        
        # DYNAMIC ELEMENTS
        dynamic_examples = {
            "wait_for_element": page.locator("#dynamic-content").wait_for(),
            "wait_for_state": page.locator(".loading").wait_for(state="hidden"),
            "custom_timeout": page.locator("#slow-element").wait_for(timeout=10000),
            
            # Проверки состояний
            "is_visible": page.locator(".tooltip").is_visible(),
            "is_enabled": page.locator("#submit-btn").is_enabled(),
            "is_checked": page.locator("#agree-checkbox").is_checked()
        }
        
        # TEXT-BASED LOCATORS
        text_examples = {
            "exact_match": page.locator("text=Exact Text Match"),
            "case_insensitive": page.locator("text=login button").first,
            "regex_matching": page.locator("text=/^Submit/i"),
            "partial_text": page.locator("text=Submit").first
        }
        
        return {
            "chain_locators": chain_examples,
            "dynamic_elements": dynamic_examples,
            "text_locators": text_examples
        }

# ЛУЧШИЕ ПРАКТИКИ ДЛЯ ЛОКАТОРОВ:
locator_best_practices = [
    "Используйте data-testid атрибуты для тестов",
    "Предпочитайте CSS селекторы XPath",
    "Создавайте стабильные, не хрупкие локаторы",
    "Избегайте сложных XPath путей",
    "Используйте осмысленные имена для локаторов",
    "Тестируйте локаторы отдельно от тестов",
    "Создавайте локаторы как свойства Page Object"
]
```

## 🏗️ Page Object Pattern

### Реализация паттерна для надежных тестов

```python
# ПОЛНАЯ РЕАЛИЗАЦИЯ PAGE OBJECT PATTERN

class PageObjectImplementation:
    def __init__(self):
        self.patterns = {}
        self.examples = {}
    
    def base_page_object(self):
        """Базовый класс для всех Page Objects"""
        
        class BasePage:
            def __init__(self, page):
                self.page = page
                self.timeout = 30000  # 30 секунд по умолчанию
            
            def navigate_to(self, url):
                """Навигация с ожиданием загрузки"""
                self.page.goto(url)
                self.wait_for_page_load()
            
            def wait_for_page_load(self):
                """Ожидание полной загрузки страницы"""
                self.page.wait_for_load_state("networkidle")
            
            def take_screenshot(self, filename=None):
                """Скриншот для отладки"""
                if filename is None:
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                
                self.page.screenshot(path=filename, full_page=True)
                return filename
            
            def get_current_url(self):
                """Получение текущего URL"""
                return self.page.url
            
            def is_element_present(self, locator):
                """Проверка наличия элемента"""
                try:
                    self.page.locator(locator).wait_for(timeout=5000)
                    return True
                except:
                    return False
        
        return BasePage
    
    def login_page_example(self):
        """Пример Page Object для страницы логина"""
        
        class LoginPage:
            def __init__(self, page):
                self.page = page
                
                # Локаторы как свойства
                self.username_field = page.locator("#username")
                self.password_field = page.locator("#password")
                self.login_button = page.locator("#login-btn")
                self.error_message = page.locator(".error-message")
                self.forgot_password_link = page.locator("text=Forgot password?")
            
            def load(self):
                """Загрузка страницы"""
                self.page.goto("https://example.com/login")
                return self
            
            def login(self, username, password):
                """Выполнение логина"""
                self.username_field.fill(username)
                self.password_field.fill(password)
                self.login_button.click()
                
                # Возвращаем следующую страницу
                from pages.dashboard_page import DashboardPage
                return DashboardPage(self.page)
            
            def login_with_validation(self, username, password):
                """Логин с валидацией"""
                # Валидация входных данных
                if not username or not password:
                    raise ValueError("Username and password are required")
                
                # Выполнение логина
                result = self.login(username, password)
                
                # Проверка результата
                if self.is_error_displayed():
                    raise Exception(f"Login failed: {self.get_error_message()}")
                
                return result
            
            def is_error_displayed(self):
                """Проверка отображения ошибки"""
                return self.error_message.is_visible()
            
            def get_error_message(self):
                """Получение текста ошибки"""
                if self.is_error_displayed():
                    return self.error_message.text_content()
                return None
            
            def click_forgot_password(self):
                """Клик по ссылке восстановления пароля"""
                self.forgot_password_link.click()
                from pages.reset_password_page import ResetPasswordPage
                return ResetPasswordPage(self.page)
        
        return LoginPage
    
    def component_object_pattern(self):
        """Component Object для повторно используемых компонентов"""
        
        class NavigationMenu:
            def __init__(self, page):
                self.page = page
                self.menu_items = page.locator(".nav-item")
                self.user_menu = page.locator("#user-menu")
                self.logout_button = page.locator("#logout-btn")
            
            def click_menu_item(self, item_text):
                """Клик по пункту меню"""
                menu_item = self.page.locator(f"text={item_text}")
                menu_item.click()
            
            def open_user_menu(self):
                """Открытие пользовательского меню"""
                self.user_menu.click()
            
            def logout(self):
                """Выход из системы"""
                self.open_user_menu()
                self.logout_button.click()
        
        class SearchComponent:
            def __init__(self, page):
                self.page = page
                self.search_input = page.locator("#search-input")
                self.search_button = page.locator("#search-btn")
                self.search_results = page.locator(".search-results")
            
            def search(self, query):
                """Выполнение поиска"""
                self.search_input.fill(query)
                self.search_button.click()
                self.search_results.wait_for()
            
            def get_search_results(self):
                """Получение результатов поиска"""
                return self.search_results.all_inner_texts()
        
        return {
            "NavigationMenu": NavigationMenu,
            "SearchComponent": SearchComponent
        }

# ЛУЧШИЕ ПРАКТИКИ PAGE OBJECT:
page_object_best_practices = [
    "Один класс = одна страница/компонент",
    "Локаторы как свойства класса",
    "Методы возвращают следующую страницу",
    "Избегайте sleeps, используйте wait",
    "Обрабатывайте ошибки и исключения",
    "Создавайте базовый класс для общих методов",
    "Используйте осмысленные имена методов",
    "Разделяйте локаторы и бизнес-логику"
]
```

## 🧪 Практические примеры тестов

### Создание надежных тестовых сценариев

```python
# ПРАКТИЧЕСКИЕ ПРИМЕРЫ ТЕСТОВ С PLAYWRIGHT

class PracticalTestExamples:
    def login_test_scenario(self):
        """Полный сценарий тестирования логина"""
        
        import pytest
        from pages.login_page import LoginPage
        from pages.dashboard_page import DashboardPage
        
        @pytest.mark.parametrize("username,password,expected_result", [
            ("valid_user", "correct_password", "success"),
            ("invalid_user", "wrong_password", "failure"),
            ("", "password", "validation_error"),
            ("user", "", "validation_error")
        ])
        def test_login_scenarios(page, username, password, expected_result):
            # ARRANGE
            login_page = LoginPage(page)
            login_page.load()
            
            # ACT
            if expected_result == "success":
                dashboard_page = login_page.login(username, password)
            else:
                try:
                    login_page.login(username, password)
                except Exception:
                    pass  # Ожидаем ошибку
            
            # ASSERT
            if expected_result == "success":
                assert isinstance(dashboard_page, DashboardPage)
                assert dashboard_page.is_loaded()
                assert "dashboard" in page.url
            else:
                assert login_page.is_error_displayed()
                error_msg = login_page.get_error_message()
                assert error_msg is not None
                
                if expected_result == "validation_error":
                    assert "required" in error_msg.lower()
        
        return test_login_scenarios
    
    def e2e_checkout_flow(self):
        """End-to-end сценарий оформления заказа"""
        
        def test_complete_checkout_flow(page):
            # 1. Авторизация
            login_page = LoginPage(page)
            dashboard = login_page.login("customer@test.com", "password123")
            
            # 2. Поиск товара
            search = dashboard.get_search_component()
            search.search("laptop")
            
            # 3. Добавление в корзину
            product_page = search.click_first_result()
            cart_page = product_page.add_to_cart(quantity=2)
            
            # 4. Оформление заказа
            checkout_page = cart_page.proceed_to_checkout()
            checkout_page.fill_shipping_address({
                "name": "Иван Иванов",
                "address": "ул. Ленина 1",
                "city": "Москва",
                "zip": "123456"
            })
            
            # 5. Выбор способа оплаты
            checkout_page.select_payment_method("credit_card")
            checkout_page.fill_payment_details({
                "card_number": "4111111111111111",
                "expiry": "12/25",
                "cvv": "123"
            })
            
            # 6. Подтверждение заказа
            confirmation_page = checkout_page.place_order()
            
            # Проверки
            assert confirmation_page.is_order_confirmed()
            assert confirmation_page.get_order_number() is not None
            assert confirmation_page.get_total_amount() > 0
        
        return test_complete_checkout_flow
    
    def data_driven_testing(self):
        """Тестирование с различными наборами данных"""
        
        import json
        from pathlib import Path
        
        def load_test_data():
            """Загрузка тестовых данных из файла"""
            data_file = Path("test_data/users.json")
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        @pytest.mark.parametrize("user_data", load_test_data())
        def test_user_registration_variations(page, user_data):
            registration_page = RegistrationPage(page)
            registration_page.load()
            
            # Заполнение формы
            registration_page.fill_form({
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "email": user_data["email"],
                "password": user_data["password"],
                "confirm_password": user_data["password"],
                "phone": user_data.get("phone", ""),
                "birth_date": user_data.get("birth_date", "")
            })
            
            # Отправка формы
            success_page = registration_page.submit()
            
            # Проверки
            if user_data["expected_result"] == "success":
                assert success_page.is_registration_successful()
                assert success_page.get_welcome_message() is not None
            else:
                assert registration_page.has_validation_errors()
                error_messages = registration_page.get_error_messages()
                assert len(error_messages) > 0
        
        return test_user_registration_variations

# ОБРАБОТКА ОШИБОК И ОТЛАДКА:
debugging_techniques = [
    "Используйте headed режим для отладки",
    "Добавляйте скриншоты при ошибках",
    "Логгируйте важные шаги теста",
    "Используйте page.pause() для интерактивной отладки",
    "Проверяйте состояние страницы после каждого шага",
    "Используйте tracing для анализа выполнения"
]
```

## ❓ Ответы на вопросы студентов

### Технические вопросы по Playwright

**Q: В чем разница между page.click() и locator.click()?**

A: 
```python
# LOCATOR.CLICK() - рекомендуемый способ
def recommended_click_example(page):
    # Locator автоматически ждет появления элемента
    page.locator("#submit-button").click()
    # Автоматически ждет кликабельности
    # Автоматически повторяет при необходимости

# PAGE.CLICK() - устаревший способ
def legacy_click_example(page):
    # Требует явного ожидания
    page.wait_for_selector("#submit-button")
    page.click("#submit-button")
    # Менее надежный, больше кода

# Практическая рекомендация:
best_practice = """
Всегда используйте locator.click() вместо page.click().
Это делает тесты более надежными и читаемыми.
"""
```

**Q: Как обрабатывать динамические элементы?**

A:
```python
# ОБРАБОТКА ДИНАМИЧЕСКИХ ЭЛЕМЕНТОВ

class DynamicElementsHandling:
    def wait_for_dynamic_content(self, page):
        """Ожидание динамического контента"""
        
        # Автоматическое ожидание
        page.locator(".dynamic-element").click()  # Авто-wait
        
        # Явное ожидание состояния
        page.locator("#loading-spinner").wait_for(state="hidden")
        
        # Пользовательский timeout
        try:
            page.locator(".ajax-content").wait_for(timeout=15000)
        except TimeoutError:
            # Обработка таймаута
            page.reload()
            page.locator(".ajax-content").wait_for(timeout=15000)
    
    def handle_flaky_elements(self, page):
        """Работа с нестабильными элементами"""
        
        # Retry mechanism
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                page.locator("#unstable-button").click()
                break
            except:
                if attempt == max_attempts - 1:
                    raise
                page.wait_for_timeout(1000)  # Wait before retry
    
    def polling_approach(self, page):
        """Подход с опросом"""
        
        import time
        
        def wait_for_condition(condition_func, timeout=30):
            start_time = time.time()
            while time.time() - start_time < timeout:
                if condition_func():
                    return True
                time.sleep(0.5)
            return False
        
        # Использование
        is_loaded = wait_for_condition(
            lambda: page.locator(".content").is_visible(),
            timeout=30
        )

# ЛУЧШИЕ ПРАКТИКИ ДЛЯ ДИНАМИЧЕСКИХ ЭЛЕМЕНТОВ:
dynamic_best_practices = [
    "Используйте встроенные wait механизмы Playwright",
    "Избегайте sleep(), используйте явные ожидания",
    "Применяйте retry логику для нестабильных элементов",
    "Проверяйте состояние элементов перед взаимодействием",
    "Используйте tracing для анализа проблем с timing"
]
```

## 📋 Подробный тайминг занятий

### Занятие 4.1: Введение в Playwright (90 минут)

**0-10 мин: Введение и обзор**
- Приветствие и анонс модуля
- Обзор архитектуры Playwright
- Сравнение с другими инструментами
- **Демонстрация возможностей инструмента**

**10-30 мин: Теория - Архитектура и компоненты**
- Browser, Context, Page, Locator
- Поток взаимодействия компонентов
- Преимущества Playwright
- **Живая демонстрация архитектуры**

**30-55 мин: Практика - Установка и первый тест**
- Установка Playwright и браузеров
- Написание первого теста
- Запуск в разных режимах (headless/headed)
- **Интерактивное кодирование с преподавателем**

**55-75 мин: Самостоятельная практика**
- Студенты создают свои первые тесты
- Работа с базовыми командами
- **Индивидуальная помощь преподавателя**

**75-90 мин: Закрепление и домашнее задание**
- Разбор типичных ошибок
- Ответы на вопросы
- Назначение домашнего задания
- **Анонс следующего занятия**

---
*Модуль 4 предоставляет глубокое понимание Playwright и формирует навыки создания надежных UI тестов*