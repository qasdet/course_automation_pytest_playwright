"""
pages/login_page.py - Page Object для страницы логина

Пример реализации page object для формы аутентификации.
"""

from playwright.sync_api import Page
from pages import BasePage
from typing import Optional


class LoginPage(BasePage):
    """Page Object для страницы логина"""
    
    # URL страницы
    @property
    def url(self) -> str:
        return "https://demoqa.com/login"
    
    # Ожидаемый заголовок
    @property
    def page_title(self) -> str:
        return "Login"
    
    # Локаторы элементов
    USERNAME_INPUT = "#userName"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login"
    NEW_USER_BUTTON = "#newUser"
    ERROR_MESSAGE = "#name"
    LOGOUT_BUTTON = "#submit"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self._logged_in = False
    
    def load(self) -> None:
        """Загрузка страницы логина"""
        self.navigate()
        self.log_action("Load login page")
    
    def enter_username(self, username: str) -> None:
        """Ввод имени пользователя"""
        self.fill(self.USERNAME_INPUT, username)
        self.log_action("Enter username", username)
    
    def enter_password(self, password: str) -> None:
        """Ввод пароля"""
        self.fill(self.PASSWORD_INPUT, password)
        self.log_action("Enter password", "[PROTECTED]")
    
    def click_login(self) -> None:
        """Клик по кнопке логина"""
        self.click(self.LOGIN_BUTTON)
        self.log_action("Click login button")
    
    def click_new_user(self) -> None:
        """Клик по кнопке регистрации нового пользователя"""
        self.click(self.NEW_USER_BUTTON)
        self.log_action("Click new user button")
    
    def login(self, username: str, password: str) -> None:
        """
        Полный процесс логина
        
        Args:
            username: Имя пользователя
            password: Пароль
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        self._logged_in = True
    
    def get_error_message(self) -> Optional[str]:
        """Получение сообщения об ошибке"""
        if self.is_visible(self.ERROR_MESSAGE):
            error_text = self.get_text(self.ERROR_MESSAGE)
            self.log_action("Get error message", error_text)
            return error_text
        return None
    
    def is_logged_in(self) -> bool:
        """Проверка, выполнен ли вход"""
        logged_in = self.is_visible(self.LOGOUT_BUTTON)
        self.log_assertion("User is logged in", logged_in)
        return logged_in
    
    def logout(self) -> None:
        """Выход из системы"""
        if self.is_logged_in():
            self.click(self.LOGOUT_BUTTON)
            self._logged_in = False
            self.log_action("Logout")
        else:
            self.logger.warning("Attempt to logout when not logged in")
    
    def is_new_user_button_visible(self) -> bool:
        """Проверка видимости кнопки регистрации"""
        visible = self.is_visible(self.NEW_USER_BUTTON)
        self.log_assertion("New user button is visible", visible)
        return visible
    
    def wait_for_login_success(self, timeout: int = 30000) -> None:
        """Ожидание успешного логина"""
        self.wait_for_element(self.LOGOUT_BUTTON, timeout=timeout)
        self.log_action("Wait for login success")
    
    def wait_for_error_message(self, timeout: int = 10000) -> None:
        """Ожидание сообщения об ошибке"""
        self.wait_for_element(self.ERROR_MESSAGE, timeout=timeout)
        self.log_action("Wait for error message")