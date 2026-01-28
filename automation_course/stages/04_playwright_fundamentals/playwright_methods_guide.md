# 📘 Полный гайд по методам Playwright

## 🎯 Введение

Это исчерпывающее руководство по всем методам фреймворка Playwright для автоматизации тестирования веб-приложений. Гайд охватывает все основные и продвинутые методы с примерами использования.

## 📚 Структура документа

1. [Основные методы навигации](#основные-методы-навигации)
2. [Методы работы с элементами](#методы-работы-с-элементами)
3. [Методы ожидания и синхронизации](#методы-ожидания-и-синхронизации)
4. [Методы работы с фреймами и окнами](#методы-работы-с-фреймами-и-окнами)
5. [Методы работы с файлами и загрузками](#методы-работы-с-файлами-и-загрузками)
6. [Методы эмуляции устройств](#методы-эмуляции-устройств)
7. [Методы работы с сетью](#методы-работы-с-сетью)
8. [Методы отладки и логирования](#методы-отладки-и-логирования)

---

## 🧭 Основные методы навигации

### `page.goto(url[, options])`
Переходит по указанному URL.

```python
# Базовое использование
await page.goto("https://example.com")

# С опциями
await page.goto("https://example.com", {
    "wait_until": "networkidle",  # load, domcontentloaded, networkidle, commit
    "timeout": 30000
})

# Ожидание разных состояний загрузки
await page.goto("https://example.com", {"wait_until": "load"})          # Ждать полной загрузки
await page.goto("https://example.com", {"wait_until": "domcontentloaded"}) # Ждать DOM
await page.goto("https://example.com", {"wait_until": "networkidle"})   # Ждать завершения сетевых запросов
```

### `page.reload([options])`
Перезагружает текущую страницу.

```python
# Простая перезагрузка
await page.reload()

# С опциями
await page.reload({
    "wait_until": "networkidle",
    "timeout": 10000
})
```

### `page.goBack([options])`
Переходит на предыдущую страницу в истории.

```python
# Простой переход назад
await page.go_back()

# С опциями
await page.go_back({
    "wait_until": "domcontentloaded"
})
```

### `page.goForward([options])`
Переходит на следующую страницу в истории.

```python
# Простой переход вперед
await page.go_forward()

# С опциями
await page.go_forward({
    "wait_until": "load"
})
```

### `page.waitForURL(url[, options])`
Ждет, пока страница не перейдет по указанному URL.

```python
# Ждать конкретный URL
await page.wait_for_url("https://example.com/dashboard")

# С паттерном
await page.wait_for_url("**/dashboard")

# С опциями
await page.wait_for_url("https://example.com/**", {
    "timeout": 5000,
    "wait_until": "networkidle"
})
```

---

## 🎯 Методы работы с элементами

### Поиск элементов

#### `page.locator(selector)`
Создает локатор для поиска элементов.

```python
# Базовый поиск
locator = page.locator("#submit-button")

# Поиск по тексту
locator = page.locator("text=Submit")

# Поиск по XPath
locator = page.locator("xpath=//button[@id='submit']")

# Поиск по CSS с атрибутами
locator = page.locator("input[type='email'][name='email']")
```

#### `page.query_selector(selector)`
Возвращает первый найденный элемент или None.

```python
# Поиск одного элемента
element = await page.query_selector("#username")
if element:
    await element.fill("testuser")
```

#### `page.query_selector_all(selector)`
Возвращает список всех найденных элементов.

```python
# Поиск всех элементов
elements = await page.query_selector_all(".item")
for element in elements:
    text = await element.text_content()
    print(text)
```

### Действия с элементами

#### `locator.click([options])`
Кликает по элементу.

```python
# Простой клик
await page.locator("#submit").click()

# Клик с опциями
await page.locator("#submit").click({
    "button": "left",      # left, right, middle
    "click_count": 1,      # количество кликов
    "delay": 100,          # задержка между кликами
    "force": False,        # игнорировать видимость
    "no_wait_after": False # не ждать после действия
})

# Клик в определенную позицию
await page.locator("#canvas").click(position={"x": 100, "y": 200})
```

#### `locator.fill(value[, options])`
Заполняет input элемент значением.

```python
# Заполнение поля
await page.locator("#email").fill("user@example.com")

# С опциями
await page.locator("#email").fill("user@example.com", {
    "force": True,    # игнорировать видимость
    "timeout": 5000   # таймаут
})
```

#### `locator.type(text[, options])`
Вводит текст посимвольно (имитирует печать пользователя).

```python
# Постепенный ввод
await page.locator("#password").type("mypassword")

# С задержкой между символами
await page.locator("#search").type("playwright", {
    "delay": 100  # 100ms между символами
})
```

#### `locator.press(key[, options])`
Нажимает клавишу на элементе.

```python
# Нажатие Enter
await page.locator("#search-input").press("Enter")

# Комбинации клавиш
await page.locator("#editor").press("Control+A")
await page.locator("#editor").press("Delete")

# Специальные клавиши
await page.locator("input").press("Tab")
await page.locator("textarea").press("Escape")
```

#### `locator.check([options])`
Отмечает checkbox/radio button.

```python
# Отметить чекбокс
await page.locator("#agree-checkbox").check()

# Убедиться, что отмечен
await page.locator("#newsletter").check({"force": True})
```

#### `locator.uncheck([options])`
Снимает отметку с checkbox/radio button.

```python
# Снять отметку
await page.locator("#notifications").uncheck()
```

#### `locator.select_option(values[, options])`
Выбирает опции в select элементе.

```python
# Выбор по значению
await page.locator("#country").select_option("US")

# Выбор нескольких опций
await page.locator("#categories").select_option(["tech", "sports"])

# Выбор по тексту
await page.locator("#size").select_option(label="Large")

# Выбор по индексу
await page.locator("#rating").select_option(index=2)
```

#### `locator.hover([options])`
Наводит курсор на элемент.

```python
# Наведение курсора
await page.locator("#tooltip-trigger").hover()

# С опциями
await page.locator("#menu-item").hover({
    "position": {"x": 10, "y": 15},
    "force": True
})
```

#### `locator.focus()`
Устанавливает фокус на элемент.

```python
# Установка фокуса
await page.locator("#search-box").focus()
```

#### `locator.blur()`
Убирает фокус с элемента.

```python
# Снятие фокуса
await page.locator("#input-field").blur()
```

### Получение информации об элементах

#### `locator.text_content([options])`
Получает текстовое содержимое элемента.

```python
# Получение текста
text = await page.locator("#title").text_content()

# С опциями
text = await page.locator(".message").text_content({
    "timeout": 3000
})
```

#### `locator.inner_text([options])`
Получает внутренний текст элемента (видимый пользователю).

```python
# Получение видимого текста
visible_text = await page.locator("#content").inner_text()
```

#### `locator.inner_html([options])`
Получает HTML содержимое элемента.

```python
# Получение HTML
html = await page.locator("#container").inner_html()
```

#### `locator.get_attribute(name[, options])`
Получает значение атрибута элемента.

```python
# Получение атрибутов
href = await page.locator("a").get_attribute("href")
class_name = await page.locator("div").get_attribute("class")
data_value = await page.locator("[data-id]").get_attribute("data-id")
```

#### `locator.input_value([options])`
Получает значение input/select/textarea элемента.

```python
# Получение значения поля ввода
value = await page.locator("#username").input_value()
```

#### `locator.is_visible([options])`
Проверяет, виден ли элемент.

```python
# Проверка видимости
if await page.locator("#modal").is_visible():
    print("Modal is visible")

# С таймаутом
is_visible = await page.locator("#tooltip").is_visible({
    "timeout": 2000
})
```

#### `locator.is_enabled([options])`
Проверяет, включен ли элемент.

```python
# Проверка доступности
if await page.locator("#submit-btn").is_enabled():
    await page.locator("#submit-btn").click()
```

#### `locator.is_checked([options])`
Проверяет, отмечен ли checkbox/radio button.

```python
# Проверка состояния чекбокса
if await page.locator("#terms").is_checked():
    print("Terms accepted")
```

#### `locator.bounding_box([options])`
Получает координаты и размеры элемента.

```python
# Получение размеров
box = await page.locator("#button").bounding_box()
if box:
    print(f"X: {box['x']}, Y: {box['y']}")
    print(f"Width: {box['width']}, Height: {box['height']}")
```

#### `locator.screenshot([options])`
Делает скриншот элемента.

```python
# Скриншот элемента
await page.locator("#chart").screenshot(path="chart.png")

# С опциями
await page.locator(".widget").screenshot({
    "path": "widget.png",
    "omit_background": True,
    "quality": 80
})
```

---

## ⏱️ Методы ожидания и синхронизации

### `page.wait_for_load_state([state, options])`
Ждет определенного состояния загрузки страницы.

```python
# Ждать полной загрузки
await page.wait_for_load_state("load")

# Ждать загрузки DOM
await page.wait_for_load_state("domcontentloaded")

# Ждать завершения сетевых запросов
await page.wait_for_load_state("networkidle")

# Ждать коммита навигации
await page.wait_for_load_state("commit")
```

### `page.wait_for_timeout(timeout)`
Ждет указанное количество миллисекунд.

```python
# Простая пауза
await page.wait_for_timeout(2000)  # 2 секунды

# Пауза между действиями
await page.locator("#button").click()
await page.wait_for_timeout(1000)  # Ждать 1 секунду
await page.locator("#result").is_visible()
```

### `locator.wait_for([options])`
Ждет, пока элемент не станет видимым/доступным.

```python
# Ждать видимости элемента
await page.locator("#loading-spinner").wait_for(state="hidden")

# Ждать появления элемента
await page.locator("#new-item").wait_for(state="visible")

# Ждать доступности элемента
await page.locator("#submit-btn").wait_for(state="enabled")

# С таймаутом
await page.locator(".popup").wait_for({
    "state": "visible",
    "timeout": 5000
})
```

### `page.expect_response(urlOrPredicate[, options])`
Ждет HTTP ответа.

```python
# Ждать конкретного ответа
async with page.expect_response("https://api.example.com/users") as response_info:
    await page.locator("#load-users").click()
response = await response_info.value
assert response.status == 200

# Ждать ответа по условию
async with page.expect_response(lambda response: response.url.endswith("/login") and response.status == 200) as response_info:
    await page.locator("#login-form").submit()
```

### `page.expect_request(urlOrPredicate[, options])`
Ждет HTTP запроса.

```python
# Ждать запроса
async with page.expect_request("https://api.example.com/login") as request_info:
    await page.locator("#login-btn").click()
request = await request_info.value
print(f"Request method: {request.method}")

# Ждать запроса по условию
async with page.expect_request(lambda request: request.resource_type == "xhr") as request_info:
    await page.locator("#refresh-data").click()
```

### `page.expect_popup([options])`
Ждет открытия нового popup окна.

```python
# Ждать popup
async with page.expect_popup() as popup_info:
    await page.locator("#open-popup").click()
popup = await popup_info.value
await popup.wait_for_load_state()
print(await popup.title())
```

### `page.expect_download([options])`
Ждет скачивания файла.

```python
# Ждать загрузки файла
async with page.expect_download() as download_info:
    await page.locator("#download-btn").click()
download = await download_info.value
print(f"Downloaded: {download.suggested_filename}")
await download.save_as("downloaded_file.pdf")
```

---

## 🖼️ Методы работы с фреймами и окнами

### Работа с фреймами

#### `page.frame(name_or_attrs)`
Получает фрейм по имени или атрибутам.

```python
# По имени
frame = page.frame("iframe-name")
await frame.locator("#button").click()

# По URL
frame = page.frame(url="https://third-party.com/widget")
await frame.wait_for_load_state()

# По селектору
frame = page.frame_locator("iframe[src*='youtube']").content_frame()
```

#### `locator.content_frame()`
Получает содержимое iframe.

```python
# Получение содержимого фрейма
iframe = page.locator("iframe.embedded-content")
frame = await iframe.content_frame()
await frame.locator("#inner-button").click()
```

### Работа с окнами и вкладками

#### `page.context.pages`
Получает все открытые страницы.

```python
# Получение всех страниц
pages = page.context.pages
print(f"Total pages: {len(pages)}")

# Переключение между страницами
if len(pages) > 1:
    new_page = pages[1]
    await new_page.bring_to_front()
    print(await new_page.title())
```

#### `page.on("popup", handler)`
Обработчик для новых popup окон.

```python
# Обработка popup
async def handle_popup(popup):
    await popup.wait_for_load_state()
    print(f"Popup title: {await popup.title()}")
    await popup.close()

page.on("popup", handle_popup)
await page.locator("#open-window").click()
```

#### `page.bring_to_front()`
Переводит страницу на передний план.

```python
# Перевести страницу вперед
await page.bring_to_front()
```

---

## 📁 Методы работы с файлами и загрузками

### Загрузка файлов

#### `locator.set_input_files(files[, options])`
Устанавливает файлы для input типа file.

```python
# Загрузка одного файла
await page.locator("#avatar-upload").set_input_files("avatar.jpg")

# Загрузка нескольких файлов
await page.locator("#document-upload").set_input_files([
    "doc1.pdf",
    "doc2.pdf"
])

# Загрузка с данными файла
await page.locator("#file-input").set_input_files({
    "name": "test.txt",
    "mimeType": "text/plain",
    "buffer": b"Hello World"
})
```

### Скачивание файлов

#### `page.on("download", handler)`
Обработчик для скачиваемых файлов.

```python
# Обработка скачивания
downloads = []

async def handle_download(download):
    downloads.append(download)
    print(f"Downloading: {download.suggested_filename}")
    await download.save_as(f"./downloads/{download.suggested_filename}")

page.on("download", handle_download)

# Инициировать скачивание
await page.locator("#export-btn").click()

# Работа со скачанными файлами
for download in downloads:
    path = await download.path()
    print(f"Saved to: {path}")
```

### Drag and Drop

#### `locator.drag_to(target[, options])`
Перетаскивает элемент на другой элемент.

```python
# Простое перетаскивание
await page.locator("#draggable").drag_to(page.locator("#droppable"))

# Перетаскивание с опциями
await page.locator(".item").drag_to(page.locator(".target"), {
    "force": True,
    "no_wait_after": True
})
```

---

## 📱 Методы эмуляции устройств

### Эмуляция мобильных устройств

#### `page.emulate_viewport(width, height)`
Эмулирует viewport устройства.

```python
# Эмуляция мобильного экрана
await page.emulate_viewport(375, 812)  # iPhone X

# Эмуляция планшета
await page.emulate_viewport(768, 1024)  # iPad

# Эмуляция desktop
await page.emulate_viewport(1920, 1080)  # Full HD
```

#### `browser.new_context([options])`
Создает контекст с эмуляцией устройства.

```python
# Эмуляция iPhone
iphone_context = await browser.new_context(
    **playwright.devices["iPhone 12 Pro"]
)
iphone_page = await iphone_context.new_page()

# Эмуляция Pixel
pixel_context = await browser.new_context(
    **playwright.devices["Pixel 5"]
)
pixel_page = await pixel_context.new_page()
```

### Эмуляция геолокации

#### `context.grant_permissions(permissions)`
Предоставляет разрешения контексту.

```python
# Предоставить доступ к геолокации
await context.grant_permissions(["geolocation"])

# Установить геолокацию
await context.set_geolocation({"latitude": 41.8902, "longitude": 12.4923})  # Rome
```

### Эмуляция сети

#### `context.set_offline(offline)`
Переводит контекст в офлайн режим.

```python
# Офлайн режим
await context.set_offline(True)
await page.goto("https://example.com")  # Будет ошибка

# Онлайн режим
await context.set_offline(False)
```

#### `context.set_extra_http_headers(headers)`
Устанавливает дополнительные HTTP заголовки.

```python
# Установка заголовков
await context.set_extra_http_headers({
    "X-Custom-Header": "test-value",
    "Authorization": "Bearer token123"
})
```

---

## 🌐 Методы работы с сетью

### Перехват и модификация запросов

#### `page.route(url, handler)`
Перехватывает сетевые запросы.

```python
# Перехват всех запросов
async def log_request(route, request):
    print(f"Request: {request.method} {request.url}")
    await route.continue_()

await page.route("**/*", log_request)

# Модификация запросов
async def modify_request(route, request):
    headers = {
        **request.headers,
        "X-Modified-Header": "modified-value"
    }
    await route.continue_(headers=headers)

await page.route("**/api/**", modify_request)
```

#### `page.unroute(url[, handler])`
Убирает перехват запросов.

```python
# Убрать перехват
await page.unroute("**/*")
```

### Мониторинг сетевых активностей

#### `page.on("request", handler)`
Обработчик для исходящих запросов.

```python
# Логирование запросов
async def log_request(request):
    print(f"→ {request.method} {request.url}")

page.on("request", log_request)
```

#### `page.on("response", handler)`
Обработчик для входящих ответов.

```python
# Логирование ответов
async def log_response(response):
    print(f"← {response.status} {response.url}")

page.on("response", log_response)
```

#### `page.on("requestfinished", handler)`
Обработчик для завершенных запросов.

```python
# Логирование завершенных запросов
async def log_finished(request):
    print(f"✓ Finished: {request.url}")

page.on("requestfinished", log_finished)
```

#### `page.on("requestfailed", handler)`
Обработчик для проваленных запросов.

```python
# Логирование проваленных запросов
async def log_failed(request):
    print(f"✗ Failed: {request.url} - {request.failure.error_text}")

page.on("requestfailed", log_failed)
```

---

## 🔍 Методы отладки и логирования

### Скриншоты

#### `page.screenshot([options])`
Делает скриншот всей страницы.

```python
# Скриншот всей страницы
await page.screenshot(path="full-page.png")

# Скриншот области
await page.screenshot(path="viewport.png", full_page=False)

# Скриншот с опциями
await page.screenshot({
    "path": "screenshot.png",
    "full_page": True,
    "omit_background": True,
    "quality": 90,
    "animations": "disabled"
})
```

### Видеозапись

#### `browser.new_context([options])`
Создает контекст с записью видео.

```python
# Запись видео
context = await browser.new_context(
    record_video_dir="videos/",
    record_video_size={"width": 1280, "height": 720}
)
page = await context.new_page()
# ... тесты ...
await context.close()  # Видео сохраняется автоматически
```

### Консоль и логи

#### `page.on("console", handler)`
Обработчик для сообщений консоли.

```python
# Логирование сообщений консоли
async def log_console(msg):
    print(f"Console: {msg.text}")

page.on("console", log_console)
```

#### `page.on("pageerror", handler)`
Обработчик для ошибок JavaScript.

```python
# Логирование ошибок страницы
async def log_error(error):
    print(f"Page Error: {error}")

page.on("pageerror", log_error)
```

### Отладка с помощью Inspector

#### Запуск с инспектором
```bash
# Запуск с инспектором
playwright test --debug

# Или программно
await page.pause()  # Останавливает выполнение для отладки
```

---

## 📋 Практические примеры использования

### Пример 1: Заполнение формы регистрации

```python
async def test_registration_form(page):
    # Переход на страницу
    await page.goto("https://example.com/register")
    
    # Ожидание загрузки формы
    await page.wait_for_load_state("networkidle")
    
    # Заполнение полей
    await page.locator("#first-name").fill("John")
    await page.locator("#last-name").fill("Doe")
    await page.locator("#email").fill("john.doe@example.com")
    await page.locator("#password").fill("securePassword123")
    
    # Выбор даты рождения
    await page.locator("#birth-date").fill("1990-01-01")
    
    # Отметить чекбоксы
    await page.locator("#terms").check()
    await page.locator("#newsletter").check()
    
    # Выбор страны
    await page.locator("#country").select_option("US")
    
    # Клик по кнопке Submit
    async with page.expect_response("**/register") as response_info:
        await page.locator("#submit-btn").click()
    
    # Проверка успешной регистрации
    response = await response_info.value
    assert response.status == 200
    
    # Проверка редиректа
    await page.wait_for_url("**/welcome")
    welcome_text = await page.locator("#welcome-message").text_content()
    assert "Welcome" in welcome_text
```

### Пример 2: Тестирование drag and drop

```python
async def test_drag_and_drop(page):
    await page.goto("https://example.com/drag-drop")
    
    # Ожидание загрузки элементов
    await page.locator("#draggable-item").wait_for(state="visible")
    await page.locator("#drop-zone").wait_for(state="visible")
    
    # Перетаскивание
    await page.locator("#draggable-item").drag_to(page.locator("#drop-zone"))
    
    # Проверка результата
    dropped_items = await page.locator("#drop-zone .item").count()
    assert dropped_items == 1
    
    # Проверка, что элемент исчез из исходного места
    draggable_visible = await page.locator("#draggable-item").is_visible()
    assert not draggable_visible
```

### Пример 3: Работа с файлами

```python
async def test_file_upload_download(page):
    await page.goto("https://example.com/file-manager")
    
    # Загрузка файла
    upload_file = "test-document.pdf"
    async with page.expect_file_chooser() as fc_info:
        await page.locator("#upload-btn").click()
    file_chooser = await fc_info.value
    await file_chooser.set_files(upload_file)
    
    # Ожидание завершения загрузки
    await page.locator(".upload-success").wait_for(state="visible")
    
    # Скачивание файла
    async with page.expect_download() as download_info:
        await page.locator("#download-link").click()
    download = await download_info.value
    
    # Проверка скачанного файла
    assert download.suggested_filename == "downloaded-file.pdf"
    await download.save_as("./downloads/actual-file.pdf")
```

### Пример 4: Тестирование мобильной версии

```python
async def test_mobile_navigation(browser):
    # Создание мобильного контекста
    context = await browser.new_context(
        **playwright.devices["iPhone 12"],
        locale="en-US",
        geolocation={"latitude": 40.7128, "longitude": -74.0060}
    )
    page = await context.new_page()
    
    await page.goto("https://example.com")
    
    # Тестирование hamburger меню
    await page.locator(".hamburger-menu").click()
    await page.locator("#mobile-nav").wait_for(state="visible")
    
    # Тестирование навигации
    await page.locator("#nav-home").click()
    await page.wait_for_url("**/home")
    
    await context.close()
```

---

## ⚠️ Советы и лучшие практики

1. **Всегда используйте явные ожидания** вместо `wait_for_timeout`
2. **Используйте локаторы** вместо `query_selector` для лучшей надежности
3. **Применяйте Page Object Model** для структурирования тестов
4. **Используйте контекстные менеджеры** для ожидания событий
5. **Настраивайте таймауты** в зависимости от сложности приложения
6. **Логируйте важные события** для отладки
7. **Используйте параллельное выполнение** для ускорения тестов
8. **Регулярно обновляйте селекторы** при изменениях в UI

---

## 📚 Дополнительные ресурсы

- [Официальная документация Playwright](https://playwright.dev/python/docs/intro)
- [Playwright Python API Reference](https://playwright.dev/python/docs/api/class-playwright)
- [Playwright Test Documentation](https://playwright.dev/python/docs/test-intro)
- [GitHub репозиторий Playwright](https://github.com/microsoft/playwright-python)

---
*Гайд будет обновляться по мере развития фреймворка Playwright*