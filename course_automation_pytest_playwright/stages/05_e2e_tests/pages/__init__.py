"""
pages/__init__.py - Инициализация пакета страниц

Этот файл содержит базовые классы и фабрики для Page Object Model.
"""

from abc import ABC, abstractmethod
from playwright.sync_api import Page, Locator
from typing import Optional, List, Dict, Any
import logging


class BasePage(ABC):
    """
    Базовый абстрактный класс для всех страниц
    
    Содержит общие методы и свойства, которые наследуют все page objects.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)
        self.default_timeout = 30000  # 30 секунд
    
    @property
    @abstractmethod
    def url(self) -> str:
        """URL страницы - должен быть реализован в наследниках"""
        pass
    
    @property
    @abstractmethod
    def page_title(self) -> str:
        """Ожидаемый заголовок страницы"""
        pass
    
    def navigate(self) -> None:
        """Навигация к странице"""
        self.logger.info(f"Navigating to {self.url}")
        self.page.goto(self.url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self) -> None:
        """Ожидание полной загрузки страницы"""
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)  # Дополнительное ожидание
    
    def get_locator(self, selector: str) -> Locator:
        """Получение локатора с базовым таймаутом"""
        return self.page.locator(selector)
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Клик по элементу"""
        timeout = timeout or self.default_timeout
        self.get_locator(selector).click(timeout=timeout)
        self.logger.debug(f"Clicked on element: {selector}")
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """Заполнение поля ввода"""
        timeout = timeout or self.default_timeout
        self.get_locator(selector).fill(value, timeout=timeout)
        self.logger.debug(f"Filled {selector} with value: {value}")
    
    def type_text(self, selector: str, text: str, delay: int = 0, timeout: Optional[int] = None) -> None:
        """Ввод текста с эмуляцией печати"""
        timeout = timeout or self.default_timeout
        self.get_locator(selector).type(text, delay=delay, timeout=timeout)
        self.logger.debug(f"Typed '{text}' into {selector}")
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Получение текста элемента"""
        timeout = timeout or self.default_timeout
        return self.get_locator(selector).text_content(timeout=timeout) or ""
    
    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """Получение атрибута элемента"""
        timeout = timeout or self.default_timeout
        return self.get_locator(selector).get_attribute(attribute, timeout=timeout)
    
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Проверка видимости элемента"""
        try:
            timeout = timeout or 5000  # Короткий таймаут для проверок
            return self.get_locator(selector).is_visible(timeout=timeout)
        except:
            return False
    
    def is_enabled(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Проверка доступности элемента"""
        try:
            timeout = timeout or 5000
            return self.get_locator(selector).is_enabled(timeout=timeout)
        except:
            return False
    
    def wait_for_element(self, selector: str, state: str = "visible", timeout: Optional[int] = None) -> None:
        """Явное ожидание элемента"""
        timeout = timeout or self.default_timeout
        self.get_locator(selector).wait_for(state=state, timeout=timeout)
        self.logger.debug(f"Element {selector} became {state}")
    
    def get_elements_count(self, selector: str) -> int:
        """Получение количества элементов"""
        return self.get_locator(selector).count()
    
    def select_option(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """Выбор опции в select"""
        timeout = timeout or self.default_timeout
        self.get_locator(selector).select_option(value=value, timeout=timeout)
        self.logger.debug(f"Selected option '{value}' in {selector}")
    
    def check(self, selector: str, timeout: Optional[int] = None) -> None:
        """Установка чекбокса"""
        timeout = timeout or self.default_timeout
        self.get_locator(selector).check(timeout=timeout)
        self.logger.debug(f"Checked {selector}")
    
    def uncheck(self, selector: str, timeout: Optional[int] = None) -> None:
        """Снятие чекбокса"""
        timeout = timeout or self.default_timeout
        self.get_locator(selector).uncheck(timeout=timeout)
        self.logger.debug(f"Unchecked {selector}")
    
    def screenshot(self, path: str, full_page: bool = False) -> None:
        """Создание скриншота страницы"""
        self.page.screenshot(path=path, full_page=full_page)
        self.logger.info(f"Screenshot saved to {path}")
    
    def execute_js(self, script: str) -> Any:
        """Выполнение JavaScript"""
        return self.page.evaluate(script)
    
    def is_page_loaded(self) -> bool:
        """Проверка загрузки страницы по заголовку"""
        try:
            return self.page_title.lower() in self.page.title().lower()
        except:
            return False


class Component(ABC):
    """
    Базовый класс для UI компонентов
    
    Используется для повторяющихся элементов интерфейса (меню, формы, виджеты).
    """
    
    def __init__(self, page: Page, root_selector: str):
        self.page = page
        self.root = page.locator(root_selector)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_locator(self, selector: str) -> Locator:
        """Получение локатора внутри компонента"""
        return self.root.locator(selector)


class PageFactory:
    """
    Фабрика для создания page objects
    
    Централизует создание страниц и обеспечивает единообразие.
    """
    
    @staticmethod
    def create_page(page_class, page_instance: Page, *args, **kwargs):
        """
        Создание экземпляра page object
        
        Args:
            page_class: Класс страницы
            page_instance: Экземпляр Playwright page
            *args: Дополнительные аргументы
            **kwargs: Дополнительные именованные аргументы
            
        Returns:
            Экземпляр page object
        """
        return page_class(page_instance, *args, **kwargs)


# Декораторы для page objects
def wait_for_page_load(func):
    """Декоратор для ожидания загрузки страницы"""
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.wait_for_page_load()
        return result
    return wrapper


def screenshot_on_error(func):
    """Декоратор для автоматических скриншотов при ошибках"""
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            # Создаем скриншот при ошибке
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/error_{func.__name__}_{timestamp}.png"
            self.screenshot(screenshot_path)
            raise e
    return wrapper


# Mixins для расширения функциональности
class WaitForElementsMixin:
    """Mixin для расширенного ожидания элементов"""
    
    def wait_for_elements_to_load(self, selectors: List[str], timeout: int = 30000):
        """Ожидание загрузки нескольких элементов"""
        for selector in selectors:
            self.wait_for_element(selector, timeout=timeout)
    
    def wait_for_any_element(self, selectors: List[str], timeout: int = 30000) -> str:
        """Ожидание появления любого из элементов"""
        with self.page.expect_event("console", timeout=timeout) as event_info:
            for selector in selectors:
                if self.is_visible(selector, timeout=1000):
                    return selector
        raise TimeoutError("None of the elements became visible")


class LoggingMixin:
    """Mixin для расширенного логирования"""
    
    def log_action(self, action: str, details: str = ""):
        """Логирование действия"""
        message = f"[ACTION] {action}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_assertion(self, assertion: str, result: bool):
        """Логирование проверки"""
        status = "PASSED" if result else "FAILED"
        self.logger.info(f"[ASSERTION] {assertion} - {status}")


# Пример использования mixins
class EnhancedBasePage(BasePage, WaitForElementsMixin, LoggingMixin):
    """Расширенный базовый класс с дополнительной функциональностью"""
    
    def __init__(self, page: Page):
        BasePage.__init__(self, page)
        # Инициализация mixins происходит автоматически