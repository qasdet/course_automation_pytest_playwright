# 📘 Полный справочник методов Playwright API

## 📋 Оглавление

1. [Browser и BrowserContext](#browser-и-browsercontext)
2. [Page методы](#page-методы)
3. [Locator методы](#locator-методы)
4. [ElementHandle методы](#elementhandle-методы)
5. [Mouse и Keyboard](#mouse-и-keyboard)
6. [Request и Response](#request-и-response)
7. [Dialog и Popup](#dialog-и-popup)
8. [Frame методы](#frame-методы)
9. [FileChooser методы](#filechooser-методы)
10. [Workers и Console](#workers-и-console)

---

## Browser и BrowserContext

### Browser методы

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Запуск браузера
    browser = p.chromium.launch(
        headless=True,           # Безголовый режим
        slow_mo=1000,           # Замедление в мс
        devtools=False,         # Открыть devtools
        args=["--no-sandbox"]   # Дополнительные аргументы
    )
    
    # Создание контекста
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},  # Размер окна
        user_agent="Custom UA",                     # User Agent
        locale="en-US",                            # Локаль
        timezone_id="Europe/London",               # Часовой пояс
        geolocation={"latitude": 51.5074, "longitude": -0.1278},  # Геолокация
        permissions=["geolocation"],               # Разрешения
        extra_http_headers={"X-Custom": "Value"}   # Заголовки
    )
    
    # Методы browser
    version = browser.version                      # Версия браузера
    browser_type = browser.browser_type            # Тип браузера
    contexts = browser.contexts                    # Список контекстов
    is_connected = browser.is_connected()          # Статус подключения
    
    # Закрытие
    browser.close()
```

### BrowserContext методы

```python
# Управление контекстом
context.close()                                    # Закрытие контекста
context.pages                                      # Список страниц
context.new_page()                                 # Создание новой страницы
context.cookies(["https://example.com"])          # Получение cookies
context.add_cookies([                              # Добавление cookies
    {
        "name": "session",
        "value": "12345",
        "domain": "example.com",
        "path": "/"
    }
])
context.clear_cookies()                           # Очистка cookies
context.grant_permissions(["camera"])             # Предоставление разрешений
context.clear_permissions()                       # Сброс разрешений

# События контекста
context.on("page", lambda page: print(f"New page: {page.url}"))
context.on("close", lambda: print("Context closed"))
```

---

## Page методы

### Навигация

```python
# Основная навигация
page.goto("https://example.com")                   # Переход по URL
page.goto("https://example.com", 
          wait_until="networkidle",               # Ожидание загрузки
          timeout=30000)                          # Таймаут

# Параметры wait_until:
# "load" - событие load (по умолчанию)
# "domcontentloaded" - событие DOMContentLoaded
# "networkidle" - отсутствие сетевой активности
# "commit" - навигация завершена

page.reload()                                      # Обновление страницы
page.go_back()                                     # Назад
page.go_forward()                                  # Вперед
page.wait_for_url("**/dashboard")                  # Ожидание URL
page.wait_for_load_state("networkidle")           # Ожидание состояния загрузки
```

### Информация о странице

```python
# Метаинформация
title = page.title()                               # Заголовок страницы
url = page.url                                     # Текущий URL
page_content = page.content()                      # HTML содержимое
viewport_size = page.viewport_size                 # Размер viewport

# Свойства страницы
is_closed = page.is_closed()                       # Закрыта ли страница
opener = page.opener                               # Родительская страница
frames = page.frames                               # Список фреймов
main_frame = page.main_frame                       # Главный фрейм
```

### Скриншоты и PDF

```python
# Скриншоты
page.screenshot(path="screenshot.png")             # Полный скриншот
page.screenshot(path="viewport.png", 
                full_page=False)                   # Только viewport
page.screenshot(path="clip.png",
                clip={"x": 0, "y": 0, "width": 500, "height": 500})  # Область

# PDF (только в Chromium)
page.pdf(path="page.pdf",
         format="A4",                             # Формат страницы
         print_background=True,                   # Фон
         margin={"top": "1cm"})                   # Поля
```

### JavaScript и оценка

```python
# Выполнение JavaScript
result = page.evaluate("() => document.title")     # Синхронное выполнение
result = page.evaluate("""                          # Многострочный код
    () => {
        return document.querySelectorAll('a').length;
    }
""")

# Выполнение с аргументами
page.evaluate("""(selector) => {
    document.querySelector(selector).click();
}""", "button.submit")

# Асинхронное выполнение
result = page.evaluate_handle("() => window")      # Возвращает JSHandle

# Ожидание выполнения функции
page.wait_for_function("""() => {
    return document.querySelector('.loaded') !== null;
}""", timeout=10000)
```

### События страницы

```python
# Обработчики событий
page.on("console", lambda msg: print(f"Console: {msg.text}"))
page.on("dialog", lambda dialog: dialog.accept())  # Обработка alert/confirm
page.on("download", lambda download: download.save_as("file.pdf"))
page.on("filechooser", lambda fc: fc.set_files("test.txt"))
page.on("popup", lambda popup: print(f"Popup opened: {popup.url}"))
page.on("request", lambda req: print(f"Request: {req.url}"))
page.on("response", lambda res: print(f"Response: {res.status}"))
page.on("websocket", lambda ws: print(f"WebSocket: {ws.url}"))

# Удаление обработчиков
page.remove_listener("console", handler_function)
```

---

## Locator методы

### Основные операции

```python
# Создание локаторов
button = page.locator("button.submit")
input_field = page.locator("input[name='email']")
text_element = page.locator("text=Submit")

# Проверки состояния
is_visible = button.is_visible()                   # Видимость
is_enabled = button.is_enabled()                   # Доступность
is_disabled = button.is_disabled()                 # Недоступность
is_editable = input_field.is_editable()            # Редактируемость
is_checked = checkbox.is_checked()                 # Состояние чекбокса

# Получение информации
count = button.count()                             # Количество элементов
text_content = button.text_content()               # Текстовое содержимое
inner_text = button.inner_text()                   # Внутренний текст
inner_html = button.inner_html()                   # Внутренний HTML
bounding_box = button.bounding_box()               # Координаты и размеры

# Атрибуты
class_attr = button.get_attribute("class")         # Получение атрибута
has_attr = button.has_attribute("disabled")        # Проверка атрибута
```

### Взаимодействие с элементами

```python
# Клик
button.click()                                     # Простой клик
button.click(force=True)                          # Принудительный клик
button.click(position={"x": 10, "y": 15})         # Клик по координатам
button.click(modifiers=["Control"])               # С модификаторами
button.click(delay=100)                           # С задержкой
button.click(button="right")                      # Правой кнопкой
button.dblclick()                                 # Двойной клик

# Ввод текста
input_field.fill("text@example.com")              # Быстрый ввод
input_field.type("Hello", delay=100)              # Постепенный ввод
input_field.clear()                               # Очистка поля

# Выбор значений
select.select_option("value1")                    # По значению
select.select_option(label="Option 1")            # По метке
select.select_option(element=option_element)      # По элементу

# Чекбоксы и радио
checkbox.check()                                  # Установка
checkbox.uncheck()                                # Снятие
radio.check()                                     # Выбор радио

# Наведение и фокус
element.hover()                                   # Наведение мыши
element.focus()                                   # Установка фокуса
element.blur()                                    # Снятие фокуса
```

### Ожидания

```python
# Явные ожидания
button.wait_for(state="visible", timeout=5000)    # Ожидание видимости
button.wait_for(state="attached")                 # Ожидание появления
button.wait_for(state="detached")                 # Ожидание исчезновения
button.wait_for(state="hidden")                   # Ожидание скрытия

# Состояния:
# "visible" - элемент видим
# "hidden" - элемент скрыт
# "stable" - элемент стабилен
# "enabled" - элемент доступен
# "disabled" - элемент недоступен
# "editable" - элемент редактируем
```

### Фильтрация и выбор

```python
# Фильтрация
visible_buttons = page.locator("button").filter(visible=True)
enabled_inputs = page.locator("input").filter(enabled=True)
checked_boxes = page.locator("input[type='checkbox']").filter(checked=True)

# По тексту
buttons_with_text = page.locator("button").filter(has_text="Submit")
exact_text = page.locator("button").filter(has_text="Submit", exact=True)

# По дочерним элементам
forms_with_submit = page.locator("form").filter(
    has=page.locator("input[type='submit']")
)

# Позиционный выбор
first_item = page.locator("li").first             # Первый элемент
last_item = page.locator("li").last               # Последний элемент
third_item = page.locator("li").nth(2)            # Третий элемент (0-based)
```

### Сложные селекторы

```python
# Chain локаторы
form = page.locator("form.login")
username = form.locator("input#username")
password = form.locator("input#password")

# Вложенные селекторы
nav_links = page.locator("nav").locator("a")
nested_elements = page.locator("div.container >> li.item")

# Комбинированные фильтры
complex_locator = page.locator("button").filter(
    visible=True
).filter(
    has_text="Submit"
).filter(
    enabled=True
)
```

---

## ElementHandle методы

```python
# Получение ElementHandle
element_handle = page.query_selector("button.submit")
elements_handles = page.query_selector_all("input")

# Основные методы (похожи на Locator, но работают с конкретным элементом)
element_handle.click()
element_handle.fill("text")
element_handle.scroll_into_view_if_needed()
element_handle.screenshot(path="element.png")

# Свойства
is_visible = element_handle.is_visible()
bounding_box = element_handle.bounding_box()
```

---

## Mouse и Keyboard

### Mouse методы

```python
mouse = page.mouse

# Основные действия
mouse.move(100, 100)                              # Перемещение
mouse.click(100, 100)                             # Клик
mouse.down()                                      # Нажатие кнопки
mouse.up()                                        # Отпускание кнопки
mouse.dblclick(100, 100)                          # Двойной клик

# Drag and Drop
mouse.move(50, 50)
mouse.down()
mouse.move(200, 200)
mouse.up()

# Скроллинг
mouse.wheel(0, 100)                               # Вертикальный скролл
mouse.wheel(100, 0)                               # Горизонтальный скролл
```

### Keyboard методы

```python
keyboard = page.keyboard

# Нажатия клавиш
keyboard.press("Enter")                           # Одиночное нажатие
keyboard.press("Control+A")                       # Комбинация
keyboard.press("F5")                              # Функциональная клавиша

# Ввод текста
keyboard.type("Hello World", delay=100)           # Постепенный ввод

# Удержание клавиш
keyboard.down("Shift")
keyboard.insert_text("hello")                     # Ввод с удержанием
keyboard.up("Shift")
```

---

## Request и Response

### Перехват запросов

```python
# Перехват и модификация запросов
page.route("**/api/data", lambda route: 
    route.fulfill(
        status=200,
        content_type="application/json",
        body='{"mock": "data"}'
    )
)

# Блокировка запросов
page.route("**/*analytics*", lambda route: route.abort())

# Модификация существующих запросов
page.route("**/api/users", lambda route, request:
    route.continue_(headers={**request.headers, "X-Custom": "Value"})
)
```

### Работа с Response

```python
# Ожидание ответа
with page.expect_response("**/api/data") as response_info:
    page.click("button.load-data")
response = response_info.value

# Информация о ответе
status = response.status                           # HTTP статус
status_text = response.status_text                 # Текст статуса
headers = response.headers                         # Заголовки
body = response.body()                             # Тело ответа
json_data = response.json()                        # JSON ответ
text_data = response.text()                        # Текст ответа
url = response.url                                 # URL ответа
```

### Мониторинг сетевых событий

```python
page.on("request", lambda request: 
    print(f"→ {request.method} {request.url}")
)

page.on("response", lambda response: 
    print(f"← {response.status} {response.url}")
)

page.on("requestfinished", lambda request: 
    print(f"✓ Finished: {request.url}")
)

page.on("requestfailed", lambda request: 
    print(f"✗ Failed: {request.url}")
)
```

---

## Dialog и Popup

### Работа с диалогами

```python
# Обработка alert/confirm/prompt
page.on("dialog", lambda dialog: 
    print(f"Dialog type: {dialog.type}")
    print(f"Message: {dialog.message}")
    dialog.accept()  # или dialog.dismiss()
    # Для prompt: dialog.accept("user input")
)

# Типы диалогов:
# "alert" - простое уведомление
# "confirm" - подтверждение (OK/Cancel)
# "prompt" - ввод текста
# "beforeunload" - предупреждение при закрытии
```

### Работа с popup окнами

```python
# Ожидание popup
with page.expect_popup() as popup_info:
    page.click("a[target='_blank']")
popup = popup_info.value

# Работа с popup
popup.wait_for_load_state()
popup_title = popup.title()
popup.close()

# События popup
page.on("popup", lambda popup: 
    print(f"Popup opened: {popup.url}")
    popup.on("close", lambda: print("Popup closed"))
)
```

---

## Frame методы

```python
# Работа с фреймами
frames = page.frames                               # Все фреймы
main_frame = page.main_frame                       # Главный фрейм

# Поиск фреймов
frame_by_name = page.frame("frame-name")
frame_by_url = page.frame(url="**/embedded*")

# Frame Locator (для iframe)
frame_locator = page.frame_locator("iframe[src*='youtube']")
frame_button = frame_locator.locator("button.play")
frame_button.click()

# Методы фрейма (аналогичны Page)
frame_title = frame.title()
frame_content = frame.content()
frame.locator("button").click()
```

---

## FileChooser методы

```python
# Обработка выбора файлов
with page.expect_file_chooser() as fc_info:
    page.click("input[type='file']")
file_chooser = fc_info.value

# Работа с FileChooser
file_chooser.set_files("path/to/file.txt")         # Один файл
file_chooser.set_files(["file1.txt", "file2.txt"]) # Несколько файлов

# Свойства FileChooser
is_multiple = file_chooser.is_multiple()           # Множественный выбор
```

---

## Workers и Console

### Web Workers

```python
# Работа с Web Workers
worker = page.workers[0]                          # Получение worker
worker_url = worker.url                           # URL worker

# Выполнение кода в worker
result = worker.evaluate("() => self.postMessage('hello')")
```

### Консоль

```python
# Перехват сообщений консоли
page.on("console", lambda msg: 
    print(f"[{msg.type}] {msg.text}")
    for arg in msg.args:
        print(f"  Arg: {arg.json_value()}")
)

# Типы сообщений консоли:
# "log", "debug", "info", "error", "warning", "dir", "dirxml"
```

---

## 💡 Практические примеры использования

### Пример 1: Комплексное взаимодействие

```python
def test_complete_user_flow(page):
    # 1. Навигация
    page.goto("https://ecommerce-site.com")
    page.wait_for_load_state("networkidle")
    
    # 2. Поиск и взаимодействие
    search_input = page.locator("input.search")
    search_input.fill("laptop")
    search_input.press("Enter")
    
    # 3. Ожидание результатов
    page.wait_for_selector(".product-grid")
    products = page.locator(".product-card")
    
    # 4. Выбор товара
    first_product = products.first
    first_product.click()
    
    # 5. Добавление в корзину
    add_to_cart = page.locator("button.add-to-cart")
    add_to_cart.click()
    
    # 6. Переход к оформлению
    checkout = page.locator("a.checkout")
    with page.expect_navigation():
        checkout.click()
```

### Пример 2: Работа с формами

```python
def test_form_submission(page):
    page.goto("https://forms-site.com/contact")
    
    # Заполнение формы
    page.locator("input#name").fill("John Doe")
    page.locator("input#email").fill("john@example.com")
    page.locator("textarea#message").fill("Test message")
    
    # Выбор опций
    page.locator("select#department").select_option("support")
    page.locator("input[type='checkbox']").check()
    
    # Отправка
    with page.expect_response("**/submit") as response_info:
        page.locator("button[type='submit']").click()
    
    # Проверка результата
    response = response_info.value
    assert response.status == 200
    assert "success" in page.locator(".message").text_content()
```

### Пример 3: Мобильное тестирование

```python
def test_mobile_responsiveness(browser):
    context = browser.new_context(
        viewport={"width": 375, "height": 812},    # iPhone X
        is_mobile=True,
        has_touch=True
    )
    page = context.new_page()
    
    page.goto("https://responsive-site.com")
    
    # Проверка мобильной навигации
    menu_toggle = page.locator(".mobile-menu-toggle")
    menu_toggle.click()
    
    mobile_menu = page.locator(".mobile-menu")
    assert mobile_menu.is_visible()
    
    # Тест touch взаимодействия
    page.locator("button.swipe-area").hover()
    # и т.д.
```

---

## ⚠️ Best Practices

1. **Используйте локаторы вместо ElementHandle** - они более стабильны
2. **Полагайтесь на автоматическое ожидание** - избегайте ручных sleep()
3. **Используйте семантические селекторы** - data-testid, role, text
4. **Обрабатывайте исключения правильно** - используйте try/except с конкретными ошибками
5. **Закрывайте ресурсы** - всегда закрывайте browser и context
6. **Используйте контексты для изоляции** - каждый тест в отдельном контексте

---

## 📚 Дополнительные ресурсы

- [Официальная документация API](https://playwright.dev/python/docs/api/class-page)
- [Playwright Inspector](https://playwright.dev/python/docs/inspector)
- [Codegen инструмент](https://playwright.dev/python/docs/codegen)
- [Trace Viewer](https://playwright.dev/python/docs/trace-viewer)

*Последнее обновление: Январь 2026*