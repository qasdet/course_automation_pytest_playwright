"""
test_playwright_examples.py - Практические примеры использования Playwright

Этот файл содержит различные сценарии тестирования,
демонстрирующие возможности Playwright для автоматизации браузера.
"""

import pytest
from playwright.sync_api import Page, expect
import re


class TestBasicNavigation:
    """Тесты базовой навигации и взаимодействия"""
    
    def test_simple_page_interaction(self, page: Page):
        """Тест простого взаимодействия со страницей"""
        # Переход на страницу
        page.goto("https://example.com")
        
        # Проверка заголовка
        expect(page).to_have_title(re.compile("Example"))
        
        # Проверка наличия заголовка h1
        header = page.locator("h1")
        expect(header).to_have_text("Example Domain")
        
        # Проверка ссылки
        link = page.locator("a")
        expect(link).to_have_attribute("href", "https://www.iana.org/domains/example")
    
    def test_form_interaction(self, page: Page):
        """Тест взаимодействия с формой"""
        # Используем тестовую форму (можно заменить на реальную)
        page.goto("https://httpbin.org/forms/post")
        
        # Заполнение формы
        page.locator("input[name='custname']").fill("John Doe")
        page.locator("input[name='custtel']").fill("+1234567890")
        page.locator("input[name='custemail']").fill("john@example.com")
        page.locator("textarea[name='comments']").fill("Test comment")
        
        # Выбор из радио кнопок
        page.locator("input[value='Medium']").check()
        
        # Выбор из чекбоксов
        page.locator("input[value='Bacon']").check()
        page.locator("input[value='Cheese']").check()
        
        # Отправка формы
        page.locator("form").locator("input[type='submit']").click()
        
        # Проверка результата (на реальном сайте может отличаться)
        page.wait_for_load_state("networkidle")


class TestSelectorsAndLocators:
    """Тесты различных типов селекторов"""
    
    def test_css_selectors(self, page: Page):
        """Тест CSS селекторов"""
        page.goto("https://demoqa.com/")
        
        # Поиск по ID
        cards = page.locator(".card")
        expect(cards.first).to_be_visible()
        
        # Поиск по атрибуту
        page.locator("[alt='logo']").first
        
        # Комбинированные селекторы
        page.locator("div.card.mt-4:first-child")
    
    def test_text_selectors(self, page: Page):
        """Тест текстовых селекторов"""
        page.goto("https://demoqa.com/")
        
        # Точный текст
        page.locator("text=Elements").click()
        
        # Частичный текст
        page.locator("text=Forms").click()
        
        # Текст внутри элемента
        page.locator("div >> text=Widgets").click()
    
    def test_chain_locators(self, page: Page):
        """Тест chain локаторов"""
        page.goto("https://demoqa.com/text-box")
        
        # Поиск внутри формы
        form = page.locator("#userForm")
        form.locator("#userName").fill("John Doe")
        form.locator("#userEmail").fill("john@example.com")
        form.locator("#currentAddress").fill("123 Main St")
        form.locator("#permanentAddress").fill("456 Oak Ave")
        
        # Клик по кнопке внутри формы
        form.locator("#submit").click()


class TestDynamicContent:
    """Тесты динамического контента"""
    
    def test_waiting_for_elements(self, page: Page):
        """Тест ожидания появления элементов"""
        page.goto("https://demoqa.com/dynamic-properties")
        
        # Ожидание видимости элемента
        visible_button = page.locator("#visibleAfter")
        expect(visible_button).to_be_visible(timeout=10000)
        
        # Ожидание активности элемента
        enabled_button = page.locator("#enableAfter")
        expect(enabled_button).to_be_enabled(timeout=10000)
        
        # Ожидание изменения цвета
        color_change_button = page.locator("#colorChange")
        initial_color = color_change_button.evaluate("el => getComputedStyle(el).color")
        
        # Ждем изменения цвета
        page.wait_for_function("""
            () => {
                const el = document.querySelector('#colorChange');
                return getComputedStyle(el).color !== arguments[0];
            }
        """, initial_color)
    
    def test_ajax_requests(self, page: Page):
        """Тест AJAX запросов"""
        page.goto("https://httpbin.org/")
        
        # Перехват сетевых запросов
        with page.expect_response("**/get") as response_info:
            page.goto("https://httpbin.org/get")
        
        response = response_info.value
        assert response.status == 200
        
        # Проверка содержимого ответа
        json_response = response.json()
        assert "url" in json_response


class TestFormsAndInputs:
    """Тесты форм и полей ввода"""
    
    def test_text_inputs(self, page: Page):
        """Тест текстовых полей ввода"""
        page.goto("https://demoqa.com/text-box")
        
        # Тест заполнения полей
        name_field = page.locator("#userName")
        name_field.fill("Jane Smith")
        expect(name_field).to_have_value("Jane Smith")
        
        # Тест очистки поля
        name_field.clear()
        expect(name_field).to_be_empty()
        
        # Тест посимвольного ввода
        name_field.type("John", delay=100)
        expect(name_field).to_have_value("John")
    
    def test_dropdown_select(self, page: Page):
        """Тест выпадающих списков"""
        page.goto("https://demoqa.com/select-menu")
        
        # Выбор по значению
        page.select_option("#oldSelectMenu", "2")
        
        # Выбор по тексту
        page.select_option("#oldSelectMenu", label="Aqua")
        
        # Множественный выбор (если доступен)
        # page.select_option("#cars", ["volvo", "saab"])
    
    def test_checkboxes_radiobuttons(self, page: Page):
        """Тест чекбоксов и радио кнопок"""
        page.goto("https://demoqa.com/checkbox")
        
        # Работа с древовидными чекбоксами
        page.locator(".rct-checkbox").first.click()
        
        # Проверка состояния
        home_checkbox = page.locator("#tree-node-home")
        expect(home_checkbox).to_be_checked()


class TestAdvancedInteractions:
    """Продвинутые взаимодействия"""
    
    def test_drag_and_drop(self, page: Page):
        """Тест drag and drop"""
        page.goto("https://demoqa.com/droppable")
        
        # Drag and drop
        page.drag_and_drop("#draggable", "#droppable")
        
        # Проверка результата
        drop_area = page.locator("#droppable")
        expect(drop_area).to_have_css("background-color", "rgba(70, 130, 180, 1)")
    
    def test_mouse_interactions(self, page: Page):
        """Тест взаимодействий мыши"""
        page.goto("https://demoqa.com/buttons")
        
        # Двойной клик
        double_click_btn = page.locator("#doubleClickBtn")
        double_click_btn.dblclick()
        expect(page.locator("#doubleClickMessage")).to_be_visible()
        
        # Клик правой кнопкой
        right_click_btn = page.locator("#rightClickBtn")
        right_click_btn.click(button="right")
        expect(page.locator("#rightClickMessage")).to_be_visible()
        
        # Наведение мыши
        hover_btn = page.locator(".btn-primary")
        hover_btn.hover()
    
    def test_keyboard_interactions(self, page: Page):
        """Тест взаимодействий клавиатуры"""
        page.goto("https://demoqa.com/text-box")
        
        # Ввод с нажатием Enter
        page.locator("#userName").fill("Test User")
        page.locator("#userName").press("Enter")
        
        # Комбинации клавиш
        page.locator("#userEmail").fill("test@example.com")
        page.locator("#userEmail").press("Tab")
        
        # Ctrl+A, Backspace
        page.locator("#currentAddress").fill("Some address")
        page.locator("#currentAddress").press("Control+A")
        page.locator("#currentAddress").press("Backspace")


class TestPopupsAndAlerts:
    """Тесты всплывающих окон и алертов"""
    
    def test_alert_handling(self, page: Page):
        """Тест обработки alert"""
        page.goto("https://demoqa.com/alerts")
        
        # Обработка простого alert
        page.on("dialog", lambda dialog: dialog.accept())
        page.locator("#alertButton").click()
        
        # Обработка confirm
        page.on("dialog", lambda dialog: dialog.accept())
        page.locator("#confirmButton").click()
        
        # Проверка результата confirm
        confirm_result = page.locator("#confirmResult")
        expect(confirm_result).to_have_text("You selected Ok")
        
        # Обработка prompt
        page.on("dialog", lambda dialog: dialog.accept("Test input"))
        page.locator("#promtButton").click()
        
        # Проверка введенного значения
        prompt_result = page.locator("#promptResult")
        expect(prompt_result).to_contain_text("Test input")


class TestFramesAndWindows:
    """Тесты iframe и новых окон"""
    
    def test_iframe_interaction(self, page: Page):
        """Тест работы с iframe"""
        page.goto("https://demoqa.com/frames")
        
        # Переключение в iframe
        frame = page.frame_locator("#frame1")
        frame_heading = frame.locator("#sampleHeading")
        expect(frame_heading).to_have_text("This is a sample page")
        
        # Взаимодействие внутри iframe
        frame.locator("body").click()
    
    def test_new_window_handling(self, page: Page):
        """Тест работы с новыми окнами"""
        page.goto("https://demoqa.com/browser-windows")
        
        # Открытие нового окна
        with page.context.expect_page() as new_page_info:
            page.locator("#windowButton").click()
        
        new_page = new_page_info.value
        expect(new_page).to_have_title("ToolsQA")
        new_page.close()


class TestMobileEmulation:
    """Тесты мобильной эмуляции"""
    
    @pytest.fixture
    def mobile_page(self, page: Page):
        """Фикстура для мобильной страницы"""
        page.set_viewport_size({"width": 375, "height": 812})
        return page
    
    def test_mobile_viewport(self, mobile_page: Page):
        """Тест мобильного viewport"""
        mobile_page.goto("https://demoqa.com")
        
        # Проверка размера viewport
        viewport_size = mobile_page.viewport_size
        assert viewport_size["width"] == 375
        assert viewport_size["height"] == 812
        
        # Проверка адаптивного дизайна
        # (зависит от конкретного сайта)


class TestFileOperations:
    """Тесты работы с файлами"""
    
    def test_file_upload(self, page: Page):
        """Тест загрузки файлов"""
        page.goto("https://demoqa.com/upload-download")
        
        # Загрузка файла
        upload_input = page.locator("#uploadFile")
        upload_input.set_input_files("test_file.txt")  # нужно создать тестовый файл
        
        # Проверка успешной загрузки
        upload_result = page.locator("#uploadedFilePath")
        expect(upload_result).to_be_visible()
    
    def test_file_download(self, page: Page):
        """Тест скачивания файлов"""
        page.goto("https://demoqa.com/upload-download")
        
        # Ожидание скачивания
        with page.expect_download() as download_info:
            page.locator("#downloadButton").click()
        
        download = download_info.value
        # Проверка имени файла
        assert "sampleFile" in download.suggested_filename
        
        # Сохранение файла
        download.save_as("downloaded_sampleFile.jpeg")


# Хелперы для тестов
@pytest.fixture
def demoqa_page(page: Page):
    """Фикстура для страницы DemoQA"""
    page.goto("https://demoqa.com")
    return page


@pytest.fixture
def setup_test_file():
    """Фикстура для создания тестового файла"""
    with open("test_file.txt", "w") as f:
        f.write("This is a test file for upload testing")
    yield "test_file.txt"
    # Cleanup
    import os
    try:
        os.remove("test_file.txt")
    except OSError:
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])