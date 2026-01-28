# 📋 Шпаргалка по методам Playwright API

## 🎯 Быстрый справочник по категориям

### Page Основные методы

| Категория | Метод | Назначение | Пример |
|-----------|-------|------------|---------|
| **Навигация** | `goto(url)` | Переход по URL | `page.goto("https://example.com")` |
| | `reload()` | Обновление страницы | `page.reload()` |
| | `go_back()` | Назад в истории | `page.go_back()` |
| | `go_forward()` | Вперед в истории | `page.go_forward()` |
| **Ожидание** | `wait_for_load_state()` | Ожидание загрузки | `page.wait_for_load_state("networkidle")` |
| | `wait_for_url()` | Ожидание URL | `page.wait_for_url("**/dashboard")` |
| | `wait_for_function()` | Ожидание JS функции | `page.wait_for_function("() => window.loaded")` |
| **Информация** | `title()` | Получение заголовка | `title = page.title()` |
| | `url` | Текущий URL | `current_url = page.url` |
| | `content()` | HTML содержимое | `html = page.content()` |
| | `viewport_size` | Размер viewport | `size = page.viewport_size` |

### Locator Основные методы

| Категория | Метод | Назначение | Пример |
|-----------|-------|------------|---------|
| **Создание** | `locator(selector)` | Создание локатора | `button = page.locator("button.submit")` |
| | `get_by_text()` | По тексту | `page.get_by_text("Submit")` |
| | `get_by_role()` | По ARIA роли | `page.get_by_role("button")` |
| **Проверки** | `is_visible()` | Видимость | `button.is_visible()` |
| | `is_enabled()` | Доступность | `input.is_enabled()` |
| | `is_checked()` | Состояние чекбокса | `checkbox.is_checked()` |
| **Взаимодействие** | `click()` | Клик | `button.click()` |
| | `fill()` | Ввод текста | `input.fill("text")` |
| | `type()` | Постепенный ввод | `input.type("hello", delay=100)` |
| | `select_option()` | Выбор в dropdown | `select.select_option("value")` |

### Browser/Context методы

| Категория | Метод | Назначение | Пример |
|-----------|-------|------------|---------|
| **Browser** | `launch()` | Запуск браузера | `browser = p.chromium.launch()` |
| | `new_context()` | Создание контекста | `context = browser.new_context()` |
| | `version` | Версия браузера | `ver = browser.version` |
| **Context** | `new_page()` | Создание страницы | `page = context.new_page()` |
| | `add_cookies()` | Добавление cookies | `context.add_cookies([...])` |
| | `clear_cookies()` | Очистка cookies | `context.clear_cookies()` |

## 📚 Полный список методов по объектам

### 🌐 Page Object

#### Навигация и URL
```python
page.goto(url, timeout=30000, wait_until="load")
page.reload(timeout=30000, wait_until="load")
page.go_back(timeout=30000)
page.go_forward(timeout=30000)
page.wait_for_url(url, timeout=30000)
```

#### Ожидание состояний
```python
page.wait_for_load_state(state="load|domcontentloaded|networkidle", timeout=30000)
page.wait_for_timeout(timeout)  # sleep в миллисекундах
page.wait_for_function(expression, arg1, arg2, ..., timeout=30000)
```

#### Скриншоты и PDF
```python
page.screenshot(path="screenshot.png", full_page=True, clip={x,y,width,height})
page.pdf(path="document.pdf", format="A4", print_background=True)
```

#### JavaScript выполнение
```python
page.evaluate(expression, arg1, arg2, ...)
page.evaluate_handle(expression, arg1, arg2, ...)
```

#### Информация о странице
```python
title = page.title()
url = page.url
content = page.content()
viewport = page.viewport_size
is_closed = page.is_closed()
frames = page.frames
```

#### События
```python
page.on(event_name, callback)
page.remove_listener(event_name, callback)
# События: "console", "dialog", "download", "filechooser", "popup", "request", "response"
```

### 🎯 Locator Object

#### Создание и выбор
```python
locator = page.locator(selector)
first = locator.first
last = locator.last
nth = locator.nth(index)
filtered = locator.filter(condition)
```

#### Проверки состояния
```python
locator.is_visible(timeout=30000)
locator.is_enabled(timeout=30000)
locator.is_disabled(timeout=30000)
locator.is_editable(timeout=30000)
locator.is_checked(timeout=30000)
```

#### Получение информации
```python
count = locator.count()
text = locator.text_content(timeout=30000)
inner_text = locator.inner_text(timeout=30000)
inner_html = locator.inner_html(timeout=30000)
attribute = locator.get_attribute(name, timeout=30000)
bounding_box = locator.bounding_box(timeout=30000)
```

#### Взаимодействие
```python
locator.click(timeout=30000, force=False, position={x,y})
locator.dblclick(timeout=30000)
locator.fill(value, timeout=30000)
locator.type(text, delay=0, timeout=30000)
locator.clear(timeout=30000)
locator.select_option(values, timeout=30000)
locator.check(timeout=30000)
locator.uncheck(timeout=30000)
locator.hover(timeout=30000)
locator.focus(timeout=30000)
locator.blur()
```

#### Ожидание
```python
locator.wait_for(state="visible|hidden|attached|detached|stable|enabled|disabled|editable", timeout=30000)
```

### 🖱️ Mouse Object

```python
mouse = page.mouse

mouse.move(x, y, steps=1)
mouse.click(x, y, delay=0, button="left|right|middle")
mouse.down(x, y, button="left|right|middle")
mouse.up(x, y, button="left|right|middle")
mouse.dblclick(x, y, delay=0)
mouse.wheel(delta_x, delta_y)
```

### ⌨️ Keyboard Object

```python
keyboard = page.keyboard

keyboard.down(key)
keyboard.up(key)
keyboard.press(key, delay=0)  # "Enter", "Control+A", "F5"
keyboard.type(text, delay=0)
keyboard.insert_text(text)
```

### 🌐 Request/Response

#### Request методы
```python
request.url
request.method
request.headers
request.post_data
request.post_data_json
request.response
```

#### Response методы
```python
response.status
response.status_text
response.headers
response.url
response.ok  # boolean
response.body()
response.text()
response.json()
```

#### Перехват запросов
```python
page.route(url_pattern, handler)
page.unroute(url_pattern, handler)

# Handler получает route и request объекты
route.fulfill(status=200, headers={}, body="")
route.continue_(url=new_url, method=new_method, headers=new_headers, post_data=new_data)
route.abort(error_code="failed")
```

### 🗨️ Dialog Object

```python
dialog.type  # "alert", "confirm", "prompt", "beforeunload"
dialog.message
dialog.default_value  # только для prompt
dialog.accept(prompt_text)  # для prompt передается текст
dialog.dismiss()
```

### 🖼️ Frame Object

```python
frame.title()
frame.url
frame.content()
frame.locator(selector)
frame.eval_on_selector(selector, expression)
frame.eval_on_selector_all(selector, expression)
frame.add_script_tag()
frame.add_style_tag()
```

### 🍪 Cookie Management

```python
# Получение cookies
cookies = context.cookies(urls=["https://example.com"])

# Добавление cookies
context.add_cookies([{
    "name": "session",
    "value": "123",
    "domain": "example.com",
    "path": "/",
    "expires": 1234567890,
    "http_only": True,
    "secure": True,
    "same_site": "Lax"
}])

# Очистка cookies
context.clear_cookies()
```

## ⚡ Часто используемые комбинации

### 1. Ожидание и клик
```python
# Стабильный способ клика
button = page.locator("button.submit")
button.wait_for(state="visible")
button.click()
```

### 2. Заполнение формы
```python
# Комплексное заполнение формы
page.locator("input#name").fill("John")
page.locator("input#email").fill("john@example.com")
page.locator("select#country").select_option("US")
page.locator("input[type='checkbox']").check()
page.locator("button[type='submit']").click()
```

### 3. Работа с динамическим контентом
```python
# Ожидание появления элемента
page.wait_for_selector(".dynamic-content", timeout=10000)
content = page.locator(".dynamic-content").text_content()

# Или с локатором
dynamic_element = page.locator(".dynamic-content")
dynamic_element.wait_for(state="visible")
```

### 4. Обработка загрузки файлов
```python
# Ожидание скачивания
with page.expect_download() as download_info:
    page.locator("button.download").click()
download = download_info.value
download.save_as("downloaded_file.pdf")
```

### 5. Мобильное тестирование
```python
# Создание мобильного контекста
context = browser.new_context(
    viewport={"width": 375, "height": 812},  # iPhone X
    is_mobile=True,
    has_touch=True
)
```

## 🚫 Антипаттерны и лучшие практики

### ❌ Плохо:
```python
# Избегайте sleep()
page.wait_for_timeout(5000)  # BAD

# Не используйте ElementHandle для длительных операций
element_handle = page.query_selector("button")  # Плохо для долгих тестов
```

### ✅ Хорошо:
```python
# Используйте автоматическое ожидание
button = page.locator("button")
button.click()  # Автоматически ждет видимости и доступности

# Используйте локаторы
page.locator("button.submit").click()  # Лучше и стабильнее
```

## 🎯 Коды ошибок для route.abort()

- `"aborted"` - запрос прерван
- `"accessdenied"` - доступ запрещен
- `"addressunreachable"` - адрес недоступен
- `"blockedbyclient"` - заблокировано клиентом
- `"blockedbyresponse"` - заблокировано ответом
- `"connectionaborted"` - соединение прервано
- `"connectionclosed"` - соединение закрыто
- `"connectionfailed"` - соединение не удалось
- `"connectionrefused"` - в соединении отказано
- `"connectionreset"` - соединение сброшено
- `"internetdisconnected"` - интернет отключен
- `"namenotresolved"` - имя не разрешено
- `"timedout"` - таймаут
- `"failed"` - общая ошибка

---

*Обновлено: Январь 2026*  
*Для получения полной документации см. PLAYWRIGHT_API_REFERENCE.md*