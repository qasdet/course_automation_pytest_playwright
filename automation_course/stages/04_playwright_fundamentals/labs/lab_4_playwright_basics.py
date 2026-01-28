# 🧪 Лабораторная работа 4: Основы Playwright

## Цель работы
Освоить фундаментальные возможности Playwright для автоматизации тестирования веб-приложений.

## Оборудование и ПО
- Python 3.8+
- Playwright
- Visual Studio Code или PyCharm
- Браузер Chrome/Chromium

## Теоретическая часть

Playwright - это современный фреймворк для автоматизации тестирования веб-приложений, поддерживающий Chromium, Firefox и WebKit. Основные преимущества:

✅ **Автоматическое ожидание** - элементы автоматически ждут своей готовности
✅ **Мощные селекторы** - поддержка CSS, XPath, текстовых селекторов
✅ **Multi-tab и iframe** - полноценная поддержка сложных сценариев
✅ **Mobile emulation** - тестирование мобильных версий
✅ **Network interception** - контроль сетевых запросов

## Практические задания

### Задание 1: Первые шаги с Playwright (20 баллов)

#### 1.1 Установка и настройка
```bash
pip install playwright
playwright install
```

#### 1.2 Базовый скрипт навигации
Создайте файл `test_basic_navigation.py`:

```python
from playwright.sync_api import sync_playwright

def test_navigate_to_website():
    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(headless=False)  # headless=False для визуального просмотра
        page = browser.new_page()
        
        try:
            # Переход на сайт
            page.goto("https://demo.playwright.dev/todomvc")
            
            # Проверка заголовка
            title = page.title()
            print(f"Заголовок страницы: {title}")
            assert "TodoMVC" in title
            
            # Проверка URL
            current_url = page.url
            print(f"Текущий URL: {current_url}")
            assert "todomvc" in current_url.lower()
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_navigate_to_website()
```

**Задание:** 
1. Запустите скрипт и наблюдайте за процессом
2. Измените URL на любой другой сайт и проверьте работу
3. Попробуйте запустить в headless режиме (`headless=True`)

### Задание 2: Работа с элементами (25 баллов)

Создайте файл `test_element_interaction.py`:

```python
from playwright.sync_api import sync_playwright

def test_todo_operations():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            page.goto("https://demo.playwright.dev/todomvc")
            
            # Добавление задач
            todo_input = page.locator(".new-todo")
            
            # Добавляем первую задачу
            todo_input.fill("Купить молоко")
            todo_input.press("Enter")
            
            # Добавляем вторую задачу
            todo_input.fill("Позвонить другу")
            todo_input.press("Enter")
            
            # Проверяем количество задач
            todo_items = page.locator(".todo-list li")
            count = todo_items.count()
            print(f"Количество задач: {count}")
            assert count == 2
            
            # Проверяем текст задач
            first_todo = todo_items.first
            assert "Купить молоко" in first_todo.text_content()
            
            # Отмечаем задачу как выполненную
            first_todo.locator(".toggle").click()
            
            # Проверяем, что задача зачеркнута
            completed_todo = page.locator(".todo-list li.completed")
            assert completed_todo.count() == 1
            
        finally:
            browser.close()

def test_form_filling():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Используем сайт с формами
            page.goto("https://testpages.eviltester.com/styled/basic-html-form-test.html")
            
            # Заполнение текстовых полей
            page.fill("input[name='username']", "testuser")
            page.fill("input[name='password']", "testpass")
            
            # Выбор из dropdown
            page.select_option("select[name='dropdown']", "dd1")
            
            # Выбор radio button
            page.check("input[value='rd1']")
            
            # Выбор checkbox
            page.check("input[value='cb1']")
            
            # Заполнение textarea
            page.fill("textarea[name='comments']", "Тестовый комментарий")
            
            print("Все поля формы заполнены успешно")
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_todo_operations()
    test_form_filling()
```

**Задание:**
1. Выполните оба теста
2. Добавьте проверку, что задачи действительно добавились в список
3. Реализуйте удаление задачи через контекстное меню

### Задание 3: Ожидания и assertions (20 баллов)

Создайте файл `test_expectations.py`:

```python
from playwright.sync_api import sync_playwright, expect

def test_dynamic_content():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            page.goto("https://demo.playwright.dev/todomvc")
            
            # Добавляем задачу
            page.fill(".new-todo", "Тестовая задача")
            page.press(".new-todo", "Enter")
            
            # Используем expect для проверок
            todo_item = page.locator(".todo-list li").first
            
            # Проверки с expect
            expect(todo_item).to_be_visible()
            expect(todo_item).to_contain_text("Тестовая задача")
            expect(todo_item).not_to_have_class("completed")
            
            # Отмечаем как выполненное
            todo_item.locator(".toggle").click()
            expect(todo_item).to_have_class("completed")
            
        finally:
            browser.close()

def test_network_waiting():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Ожидание конкретного ответа
            with page.expect_response("**/api/**") as response_info:
                page.goto("https://httpbin.org/get")
            
            response = response_info.value
            print(f"Статус ответа: {response.status}")
            assert response.status == 200
            
            # Ожидание загрузки элемента
            page.goto("https://demo.playwright.dev/todomvc")
            page.wait_for_selector(".new-todo", timeout=5000)
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_dynamic_content()
    test_network_waiting()
```

**Задание:**
1. Запустите тесты и изучите работу expect
2. Добавьте тест на ожидание появления alert
3. Реализуйте тест с ожиданием изменения текста элемента

### Задание 4: Работа с несколькими вкладками (15 баллов)

Создайте файл `test_multiple_tabs.py`:

```python
from playwright.sync_api import sync_playwright

def test_tab_handling():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto("https://testpages.eviltester.com/styled/windows-test.html")
            
            # Сохраняем ссылку на оригинальную вкладку
            original_page = page
            
            # Кликаем ссылку, которая открывает новую вкладку
            with context.expect_page() as new_page_info:
                page.click("a[target='_blank']")
            
            # Получаем новую вкладку
            new_page = new_page_info.value
            new_page.wait_for_load_state()
            
            print(f"Заголовок новой вкладки: {new_page.title()}")
            
            # Работаем с новой вкладкой
            new_page.fill("#name", "Тестовый пользователь")
            new_page.click("#submit")
            
            # Переключаемся обратно на оригинальную вкладку
            original_page.bring_to_front()
            print(f"Вернулись на: {original_page.title()}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_tab_handling()
```

**Задание:**
1. Выполните тест работы с вкладками
2. Добавьте закрытие вкладок и проверку количества открытых вкладок
3. Реализуйте переключение между 3+ вкладками

### Задание 5: Mobile эмуляция (20 баллов)

Создайте файл `test_mobile_emulation.py`:

```python
from playwright.sync_api import sync_playwright

def test_mobile_viewport():
    with sync_playwright() as p:
        # Эмуляция iPhone 12
        iphone_12 = p.devices["iPhone 12"]
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(**iphone_12)
        page = context.new_page()
        
        try:
            page.goto("https://google.com")
            
            # Проверяем viewport
            viewport_size = page.viewport_size
            print(f"Viewport size: {viewport_size}")
            
            # Делаем скриншот
            page.screenshot(path="mobile_screenshot.png")
            print("Скриншот сохранен как mobile_screenshot.png")
            
        finally:
            browser.close()

def test_custom_device():
    with sync_playwright() as p:
        # Создание кастомного устройства
        custom_device = {
            "user_agent": "Custom Mobile Browser",
            "viewport": {"width": 375, "height": 667},
            "device_scale_factor": 2,
            "is_mobile": True,
            "has_touch": True
        }
        
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(**custom_device)
        page = context.new_page()
        
        try:
            page.goto("https://whatismyviewport.com/")
            page.wait_for_timeout(3000)  # Ждем загрузки
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_mobile_viewport()
    test_custom_device()
```

**Задание:**
1. Выполните тесты мобильной эмуляции
2. Попробуйте разные устройства из `p.devices`
3. Сравните отображение сайта на desktop и mobile версиях

## Дополнительные задания (по желанию)

### Задание 6: Network interception (15 баллов)
Реализуйте перехват и модификацию сетевых запросов.

### Задание 7: Screenshot и PDF (10 баллов)
Создайте скриншоты разных элементов и страницы в PDF.

### Задание 8: Geolocation эмуляция (10 баллов)
Протестируйте сайт с геолокационными сервисами.

## Требования к отчету

1. **Титульный лист** с названием работы, ФИО, датой
2. **Цель работы** - краткое описание целей
3. **Ход работы** - по каждому заданию:
   - Код программы
   - Результаты выполнения
   - Скриншоты (где необходимо)
4. **Выводы** - что было освоено, сложности, выводы
5. **Ответы на контрольные вопросы**

## Контрольные вопросы

1. В чем преимущества Playwright перед Selenium?
2. Как работает автоматическое ожидание в Playwright?
3. Какие типы селекторов поддерживает Playwright?
4. В чем разница между `page.click()` и `locator.click()`?
5. Как обрабатывать множественные вкладки?
6. Для чего используется mobile эмуляция?
7. Как работают ожидания в Playwright?
8. В чем разница между `headless=True` и `headless=False`?

## Критерии оценки

- **85-100 баллов** - Все задания выполнены, код чистый, отчет полный
- **70-84 балла** - Основные задания выполнены, есть мелкие недочеты
- **50-69 баллов** - Выполнены базовые задания, требуется доработка
- **Менее 50 баллов** - Существенные недоработки

## Полезные ресурсы

- [Официальная документация Playwright](https://playwright.dev/python/)
- [Playwright Test Runner](https://playwright.dev/python/docs/intro)
- [Selector Playground](https://playwright.dev/python/docs/selectors)