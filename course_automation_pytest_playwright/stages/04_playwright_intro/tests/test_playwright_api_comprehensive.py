"""
test_playwright_api_comprehensive.py - Комплексные примеры использования всех методов Playwright API

Этот файл демонстрирует практическое применение всех основных методов Playwright API
с реальными сценариями тестирования.
"""

import pytest
import re
from playwright.sync_api import Page, expect, sync_playwright


class TestBrowserAndContext:
    """Тесты Browser и BrowserContext методов"""
    
    def test_browser_launch_options(self, browser):
        """Тест различных опций запуска браузера"""
        # Проверка версии браузера
        version = browser.version
        assert isinstance(version, str)
        assert len(version) > 0
        
        # Проверка типа браузера
        browser_type = browser.browser_type
        assert browser_type in ["chromium", "firefox", "webkit"]
    
    def test_context_creation(self, browser):
        """Тест создания контекста с различными настройками"""
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Test Automation Bot 1.0",
            locale="en-US",
            timezone_id="America/New_York"
        )
        
        page = context.new_page()
        page.goto("https://httpbin.org/headers")
        
        # Проверка user agent
        content = page.text_content("pre")
        assert "Test Automation Bot 1.0" in content
        
        context.close()
    
    def test_cookie_management(self, browser):
        """Тест управления cookies"""
        context = browser.new_context()
        
        # Добавление cookies
        context.add_cookies([{
            "name": "session_token",
            "value": "abc123",
            "domain": "httpbin.org",
            "path": "/",
            "http_only": True,
            "secure": True
        }])
        
        page = context.new_page()
        page.goto("https://httpbin.org/cookies")
        
        # Проверка cookies
        content = page.text_content("pre")
        assert "session_token" in content
        assert "abc123" in content
        
        # Получение cookies
        cookies = context.cookies(["https://httpbin.org"])
        cookie_names = [cookie["name"] for cookie in cookies]
        assert "session_token" in cookie_names
        
        context.close()


class TestPageNavigation:
    """Тесты навигации страниц"""
    
    def test_page_navigation_methods(self, page: Page):
        """Тест различных методов навигации"""
        # Базовая навигация
        page.goto("https://example.com")
        assert "Example Domain" in page.title()
        
        # Навигация с ожиданием
        page.goto("https://httpbin.org/delay/1", wait_until="networkidle")
        assert page.url == "https://httpbin.org/delay/1"
        
        # Обновление страницы
        initial_content = page.text_content("body")
        page.reload()
        reloaded_content = page.text_content("body")
        assert initial_content == reloaded_content
        
        # Навигация назад/вперед
        page.goto("https://example.com")
        first_title = page.title()
        
        page.goto("https://httpbin.org")
        second_title = page.title()
        
        page.go_back()
        assert page.title() == first_title
        
        page.go_forward()
        assert page.title() == second_title
    
    def test_wait_for_conditions(self, page: Page):
        """Тест различных условий ожидания"""
        page.goto("https://example.com")
        
        # Ожидание URL
        page.wait_for_url("**/example.com")
        
        # Ожидание состояния загрузки
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state("networkidle")
        
        # Пользовательское ожидание
        page.wait_for_function("""
            () => document.readyState === 'complete'
        """)


class TestPageInformation:
    """Тесты получения информации о странице"""
    
    def test_page_metadata(self, page: Page):
        """Тест получения метаданных страницы"""
        page.goto("https://example.com")
        
        # Заголовок
        title = page.title()
        assert isinstance(title, str)
        assert len(title) > 0
        
        # URL
        url = page.url
        assert url == "https://example.com/"
        
        # Содержимое
        content = page.content()
        assert "<html>" in content.lower()
        assert "example domain" in content.lower()
    
    def test_viewport_operations(self, page: Page):
        """Тест операций с viewport"""
        page.goto("https://example.com")
        
        # Получение размера viewport
        viewport = page.viewport_size
        assert isinstance(viewport, dict)
        assert "width" in viewport
        assert "height" in viewport
        
        # Страница не закрыта
        assert not page.is_closed()


class TestScreenshotsAndPDF:
    """Тесты скриншотов и PDF"""
    
    def test_screenshot_operations(self, page: Page):
        """Тест различных типов скриншотов"""
        page.goto("https://example.com")
        
        # Полный скриншот
        page.screenshot(path="test_full_screenshot.png", full_page=True)
        
        # Скриншот viewport
        page.screenshot(path="test_viewport_screenshot.png", full_page=False)
        
        # Скриншот области
        page.screenshot(
            path="test_clip_screenshot.png",
            clip={"x": 0, "y": 0, "width": 500, "height": 300}
        )
    
    @pytest.mark.skipif("True", reason="PDF доступен только в Chromium")
    def test_pdf_generation(self, page: Page):
        """Тест генерации PDF (только Chromium)"""
        page.goto("https://example.com")
        page.pdf(
            path="test_page.pdf",
            format="A4",
            print_background=True
        )


class TestJavaScriptEvaluation:
    """Тесты выполнения JavaScript"""
    
    def test_javascript_evaluation(self, page: Page):
        """Тест выполнения JavaScript кода"""
        page.goto("https://example.com")
        
        # Простая оценка
        title = page.evaluate("() => document.title")
        assert title == "Example Domain"
        
        # Оценка с возвратом объекта
        links_count = page.evaluate("() => document.querySelectorAll('a').length")
        assert isinstance(links_count, int)
        
        # Оценка с аргументами
        selector = "h1"
        header_text = page.evaluate("""(sel) => {
            const element = document.querySelector(sel);
            return element ? element.textContent : '';
        }""", selector)
        assert header_text == "Example Domain"
        
        # Ожидание выполнения функции
        page.goto("https://httpbin.org/delay/1")
        page.wait_for_function("() => document.readyState === 'complete'")


class TestPageEvents:
    """Тесты событий страницы"""
    
    def test_console_events(self, page: Page):
        """Тест перехвата консольных сообщений"""
        messages = []
        
        def handle_console(msg):
            messages.append({
                "type": msg.type,
                "text": msg.text
            })
        
        page.on("console", handle_console)
        
        page.goto("https://example.com")
        page.evaluate("() => console.log('Test message')")
        page.evaluate("() => console.error('Test error')")
        
        assert len(messages) >= 2
        assert any(msg["text"] == "Test message" for msg in messages)
        assert any(msg["type"] == "error" for msg in messages)
    
    def test_dialog_handling(self, page: Page):
        """Тест обработки диалогов"""
        page.goto("https://example.com")
        
        # Обработка alert
        page.on("dialog", lambda dialog: dialog.accept())
        page.evaluate("() => alert('Test alert')")
        
        # Обработка confirm
        confirm_result = []
        page.on("dialog", lambda dialog: (
            confirm_result.append(dialog.message),
            dialog.accept()
        ))
        page.evaluate("() => confirm('Test confirm')")
        assert "Test confirm" in confirm_result
    
    def test_network_events(self, page: Page):
        """Тест сетевых событий"""
        requests = []
        responses = []
        
        page.on("request", lambda req: requests.append(req.url))
        page.on("response", lambda res: responses.append(res.status))
        
        page.goto("https://example.com")
        
        assert len(requests) > 0
        assert len(responses) > 0
        assert all(isinstance(status, int) for status in responses)


class TestLocatorMethods:
    """Тесты методов Locator"""
    
    def test_locator_creation_and_basic_methods(self, page: Page):
        """Тест создания локаторов и базовых методов"""
        page.goto("https://example.com")
        
        # Создание локаторов
        header = page.locator("h1")
        link = page.locator("a")
        
        # Проверки состояния
        assert header.is_visible()
        assert link.is_visible()
        assert link.is_enabled()
        
        # Получение информации
        assert header.count() == 1
        assert "Example Domain" in header.text_content()
        assert "Example Domain" in header.inner_text()
    
    def test_locator_interactions(self, page: Page):
        """Тест взаимодействий через локаторы"""
        page.goto("https://httpbin.org/forms/post")
        
        # Ввод текста
        name_input = page.locator("input[name='custname']")
        name_input.fill("John Doe")
        assert name_input.input_value() == "John Doe"
        
        # Очистка и повторный ввод
        name_input.clear()
        name_input.type("Jane Smith", delay=50)
        assert name_input.input_value() == "Jane Smith"
        
        # Выбор опций
        # size_select = page.locator("select[name='size']")
        # size_select.select_option("medium")
    
    def test_locator_filters(self, page: Page):
        """Тест фильтрации локаторов"""
        page.goto("https://example.com")
        
        # Фильтрация по видимости
        visible_links = page.locator("a").filter(visible=True)
        assert visible_links.count() > 0
        
        # Фильтрация по тексту
        more_info_link = page.locator("a").filter(has_text="More information")
        assert more_info_link.count() == 1
        
        # Позиционный выбор
        if page.locator("a").count() > 1:
            first_link = page.locator("a").first
            last_link = page.locator("a").last
            assert first_link != last_link


class TestMouseAndKeyboard:
    """Тесты Mouse и Keyboard"""
    
    def test_mouse_operations(self, page: Page):
        """Тест операций мыши"""
        page.goto("https://example.com")
        
        # Наведение
        link = page.locator("a")
        link.hover()
        
        # Клик по координатам (если элемент видим)
        page.mouse.move(100, 100)
        # page.mouse.click(100, 100)  # Осторожно с кликами вне элементов
    
    def test_keyboard_operations(self, page: Page):
        """Тест операций клавиатуры"""
        page.goto("https://httpbin.org/forms/post")
        
        # Ввод текста
        name_input = page.locator("input[name='custname']")
        name_input.focus()
        page.keyboard.type("Test User", delay=50)
        
        # Нажатие клавиш
        page.keyboard.press("Tab")
        page.keyboard.press("Enter")


class TestNetworkInterception:
    """Тесты перехвата сетевых запросов"""
    
    def test_request_interception(self, page: Page):
        """Тест перехвата и модификации запросов"""
        # Модификация ответа
        page.route("**/robots.txt", lambda route: 
            route.fulfill(
                status=200,
                content_type="text/plain",
                body="User-agent: *\nDisallow: /"
            )
        )
        
        page.goto("https://example.com/robots.txt")
        content = page.text_content("body")
        assert "User-agent" in content
    
    def test_response_handling(self, page: Page):
        """Тест обработки ответов"""
        page.goto("https://example.com")
        
        # Ожидание и анализ ответа
        with page.expect_response("**/example.com") as response_info:
            page.reload()
        
        response = response_info.value
        assert response.status == 200
        assert "text/html" in response.headers["content-type"]


class TestFrames:
    """Тесты работы с фреймами"""
    
    def test_frame_operations(self, page: Page):
        """Тест операций с фреймами"""
        # Тест с сайтом, содержащим фреймы
        page.goto("https://www.w3schools.com/tags/tag_iframe.asp")
        
        # Получение фреймов
        frames = page.frames
        assert len(frames) > 0  # Главный фрейм + возможно iframe
        
        main_frame = page.main_frame
        assert main_frame is not None


class TestAdvancedScenarios:
    """Продвинутые сценарии тестирования"""
    
    def test_complex_user_flow(self, page: Page):
        """Тест комплексного пользовательского сценария"""
        # Сценарий: поиск -> выбор -> действие
        page.goto("https://httpbin.org")
        
        # Навигация по ссылке
        html_link = page.locator("a").filter(has_text="/html")
        html_link.click()
        
        # Проверка результата
        assert "/html" in page.url
        assert page.locator("h1").is_visible()
    
    def test_form_submission_flow(self, page: Page):
        """Тест полного сценария работы с формой"""
        page.goto("https://httpbin.org/forms/post")
        
        # Заполнение формы
        page.locator("input[name='custname']").fill("Test User")
        page.locator("input[name='custtel']").fill("123-456-7890")
        page.locator("input[name='custemail']").fill("test@example.com")
        
        # Отправка формы
        with page.expect_response("**/post") as response_info:
            page.locator("input[type='submit']").click()
        
        # Проверка результата
        response = response_info.value
        assert response.status == 200


# Фикстуры для тестов
@pytest.fixture
def browser():
    """Фикстура для браузера"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    """Фикстура для контекста"""
    context = browser.new_context()
    yield context
    context.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])