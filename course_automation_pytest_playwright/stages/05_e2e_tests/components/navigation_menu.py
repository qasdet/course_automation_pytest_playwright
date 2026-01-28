"""
components/navigation_menu.py - Component Object для навигационного меню

Пример реализации компонента для повторяющегося UI элемента.
"""

from playwright.sync_api import Page, Locator
from pages import Component
from typing import List


class NavigationMenu(Component):
    """Component Object для навигационного меню"""
    
    # Локаторы
    MENU_TOGGLE = ".burger-icon"
    MENU_CONTAINER = ".sidebar-wrapper"
    MENU_ITEMS = ".menu-list li"
    ACTIVE_ITEM = ".menu-list li.active"
    MENU_LINKS = ".menu-list a"
    
    def __init__(self, page: Page):
        super().__init__(page, self.MENU_CONTAINER)
        self.page = page
    
    def is_menu_open(self) -> bool:
        """Проверка, открыто ли меню"""
        return self.root.is_visible()
    
    def open_menu(self) -> None:
        """Открытие меню"""
        if not self.is_menu_open():
            self.page.locator(self.MENU_TOGGLE).click()
    
    def close_menu(self) -> None:
        """Закрытие меню"""
        if self.is_menu_open():
            # Клик вне меню или на toggle кнопку
            self.page.locator(self.MENU_TOGGLE).click()
    
    def get_menu_items(self) -> List[str]:
        """Получение списка пунктов меню"""
        items = self.root.locator(self.MENU_ITEMS).all()
        return [item.text_content().strip() for item in items if item.text_content()]
    
    def click_menu_item(self, item_text: str) -> None:
        """Клик по пункту меню по тексту"""
        menu_items = self.root.locator(self.MENU_LINKS)
        menu_items.filter(has_text=item_text).click()
    
    def click_menu_item_by_index(self, index: int) -> None:
        """Клик по пункту меню по индексу"""
        menu_items = self.root.locator(self.MENU_LINKS)
        if index < menu_items.count():
            menu_items.nth(index).click()
    
    def get_active_item(self) -> str:
        """Получение активного пункта меню"""
        active_item = self.root.locator(self.ACTIVE_ITEM)
        if active_item.is_visible():
            return active_item.text_content().strip()
        return ""
    
    def is_item_active(self, item_text: str) -> bool:
        """Проверка, является ли пункт активным"""
        menu_items = self.root.locator(self.MENU_LINKS)
        target_item = menu_items.filter(has_text=item_text)
        return "active" in (target_item.get_attribute("class") or "")
    
    def get_menu_links(self) -> List[str]:
        """Получение URL всех ссылок в меню"""
        links = self.root.locator(self.MENU_LINKS).all()
        return [link.get_attribute("href") or "" for link in links]


class Header(Component):
    """Component Object для хедера страницы"""
    
    HEADER_CONTAINER = ".header-wrapper"
    LOGO = ".logo"
    SEARCH_INPUT = "#searchBox"
    CART_ICON = ".shopping_cart_badge"
    USER_PROFILE = ".profile-wrapper"
    
    def __init__(self, page: Page):
        super().__init__(page, self.HEADER_CONTAINER)
        self.page = page
    
    def get_logo_text(self) -> str:
        """Получение текста логотипа"""
        return self.get_locator(self.LOGO).text_content() or ""
    
    def search(self, query: str) -> None:
        """Выполнение поиска"""
        search_input = self.get_locator(self.SEARCH_INPUT)
        search_input.fill(query)
        search_input.press("Enter")
    
    def get_cart_count(self) -> int:
        """Получение количества товаров в корзине"""
        cart_badge = self.get_locator(self.CART_ICON)
        if cart_badge.is_visible():
            count_text = cart_badge.text_content()
            try:
                return int(count_text) if count_text else 0
            except ValueError:
                return 0
        return 0
    
    def click_user_profile(self) -> None:
        """Клик по профилю пользователя"""
        self.get_locator(self.USER_PROFILE).click()
    
    def is_user_logged_in(self) -> bool:
        """Проверка, выполнен ли вход"""
        return self.get_locator(self.USER_PROFILE).is_visible()


# Фабрика компонентов
class ComponentFactory:
    """Фабрика для создания компонентов"""
    
    @staticmethod
    def create_navigation_menu(page: Page) -> NavigationMenu:
        """Создание навигационного меню"""
        return NavigationMenu(page)
    
    @staticmethod
    def create_header(page: Page) -> Header:
        """Создание хедера"""
        return Header(page)