# Модуль 5: Расширенное тестирование с Playwright

## 🎯 Цели модуля (4 недели / 16 занятий)

**По окончании модуля студент сможет:**
- Применять продвинутые техники тестирования с Playwright
- Работать с API и сетевыми запросами
- Обрабатывать файлы и загрузки
- Тестировать мобильные и адаптивные интерфейсы
- Использовать Visual Testing и сравнение скриншотов
- **Реализовывать комплексные тестовые сценарии**
- **Настраивать параллельное выполнение тестов**
- **Интегрировать тесты в CI/CD процессы**
- **Обрабатывать flaky тесты и обеспечивать стабильность**
- **Настраивать расширенные возможности отладки**
- **Реализовывать тестирование сложных пользовательских сценариев**

## 👨‍🏫 Методические материалы для преподавателя

### Продвинутые подходы к преподаванию:

**🎯 Специфика модуля:**
- **Комплексные сценарии:** От простых тестов к enterprise-level решениям
- **Реальные проблемы:** Решение типичных production issues
- **Performance awareness:** Понимание производительности тестов
- **Debugging mastery:** Продвинутые техники отладки
- **CI/CD интеграция:** Подготовка к реальной работе
- **Flaky test handling:** Обработка нестабильных тестов
- **Advanced troubleshooting:** Сложная диагностика проблем

### 🛠️ Инструменты продвинутого тестировщика

#### Расширенные расширения VS Code для продвинутого тестирования:
- **Playwright Test for VSCode** - расширенная поддержка Playwright
- **GitLens** - расширенная работа с Git
- **Thunder Client** - API тестирование прямо в IDE
- **Auto Rename Tag** - удобная работа с HTML
- **Bracket Pair Colorizer** - визуализация вложенных структур
- **Error Lens** - улучшенное отображение ошибок

#### Продвинутые команды для отладки:
```bash
# Расширенный запуск тестов с отладкой
npx playwright test --debug --headed

# Запуск с подробным логированием
npx playwright test --debug --verbose

# Генерация трассировки для анализа
npx playwright test --trace=on

# Запуск с записью видео
npx playwright test --video=on

# Открытие инспектора Playwright
npx playwright open --device="iPhone 12" https://example.com

# Генерация кода для тестов
npx playwright codegen https://example.com

# Просмотр трассировки
npx playwright show-trace trace.zip
```

#### Методы отладки сложных сценариев:
```python
# Интерактивная отладка
import pdb

def debug_complex_scenario(page):
    """Интерактивная отладка сложного сценария"""
    
    # Пауза для ручной отладки
    page.pause()
    
    # Пошаговое выполнение
    pdb.set_trace()
    
    # Логгирование всех действий
    page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
    page.on("request", lambda req: print(f"REQUEST: {req.method} {req.url}"))
    page.on("response", lambda res: print(f"RESPONSE: {res.status} {res.url}"))
    
    # Скриншот при каждой ошибке
    try:
        yield page
    except Exception as e:
        page.screenshot(path=f"error_{int(time.time())}.png")
        raise

# Использование контекстного менеджера для отладки
with debug_complex_scenario(page):
    # Ваш тестовый код здесь
    page.goto("https://complex-app.com")
    # ...
```

**📋 Требуемые ресурсы:**
- Production-like тестовые стенды
- API mock servers
- Mobile device emulators
- Performance monitoring tools
- CI/CD pipeline examples
- **Flaky test databases and scenarios**
- **Real-world bug repositories**
- **Performance bottleneck simulators**
- **Network condition emulators**

### 📋 Подробный тайминг занятий модуля 5

#### Занятие 5.1: Продвинутое API тестирование (90 минут)

**0-15 мин:** Проверка домашнего задания и review
- Разбор решений студентов по базовому API тестированию
- Обсуждение возникших проблем
- Демонстрация лучших практик

**15-35 мин:** Теория - Расширенные техники API тестирования
- Mock серверы и их применение
- Тестирование различных HTTP методов
- Обработка асинхронных ответов
- **Живая демонстрация mock сервера**

**35-60 мин:** Практика - Создание комплексных API тестов
- Настройка WireMock/MSW для мокирования
- Тестирование GraphQL API
- Обработка rate limiting и timeouts
- **Интерактивное кодирование с преподавателем**

**60-80 мин:** Самостоятельная работа
- Студенты создают тесты для реального API
- Работа с различными сценариями ошибок
- **Индивидуальная помощь преподавателя**

**80-90 мин:** Закрепление и домашнее задание
- Разбор типичных ошибок
- Ответы на вопросы
- Назначение домашнего задания
- **Анонс следующего занятия**

#### Занятие 5.2: Работа с файлами и загрузками (90 минут)

**0-10 мин:** Краткий обзор предыдущего материала

**10-30 мин:** Теория - Продвинутая работа с файлами
- Drag and drop тестирование
- Множественная загрузка файлов
- Тестирование прогресс-баров
- **Демонстрация реальных сценариев**

**30-55 мин:** Практика - Создание файловых тестов
- Тестирование разных типов файлов
- Валидация размеров и форматов
- Обработка ошибок загрузки
- **Live coding session**

**55-75 мин:** Самостоятельная практика
- Студенты создают тесты для файловых операций
- Работа с динамическим контентом
- **Персональная помощь преподавателя**

**75-90 мин:** Подведение итогов
- Проверка выполненных работ
- Ответы на вопросы
- Домашнее задание

#### Занятие 5.3: Мобильное тестирование (90 минут)

**0-15 мин:** Теория - Особенности мобильного тестирования
- Device emulation vs реальные устройства
- Touch gestures и взаимодействия
- Адаптивный дизайн тестирование
- **Сравнение подходов**

**15-40 мин:** Практика - Mobile device testing
- Настройка device descriptors
- Тестирование touch events
- Orientation change testing
- **Интерактивная демонстрация**

**40-65 мин:** Практика - Responsive design testing
- Breakpoint testing
- Cross-device compatibility
- Performance на мобильных устройствах
- **Hands-on coding**

**65-85 мин:** Самостоятельная работа
- Создание мобильных тестовых сценариев
- Тестирование адаптивности
- **Индивидуальные консультации**

**85-90 мин:** Завершение занятия
- Обзор пройденного материала
- Домашнее задание

#### Занятие 5.4: Visual Testing и скриншоты (90 минут)

**0-20 мин:** Теория - Visual regression testing
- Pixel-perfect vs perceptual testing
- Ignoring dynamic content
- Threshold settings и их влияние
- **Примеры реальных кейсов**

**20-45 мин:** Практика - Настройка visual testing
- Allure screenshots integration
- Custom screenshot strategies
- Diff comparison tools
- **Live demonstration**

**45-70 мин:** Самостоятельная практика
- Создание visual test suites
- Настройка ignore regions
- Тестирование разных viewports
- **Персональная поддержка**

**70-90 мин:** Закрепление материала
- Разбор выполненных заданий
- Ответы на вопросы
- Финальное домашнее задание модуля

**⏰ Структура продвинутых занятий:**
- 10 мин: Review предыдущего материала
- 25 мин: Advanced theory и демонстрации
- 40 мин: Complex live coding sessions
- 15 мин: Перерыв
- 20 мин: Hands-on complex scenarios
- 10 мин: Summary и homework

## 🌐 API и сетевое тестирование

### Мастерство работы с API

```python
# ПРОДВИНУТОЕ API ТЕСТИРОВАНИЕ С PLAYWRIGHT

class AdvancedAPITesting:
    def __init__(self):
        self.interception_techniques = {}
        self.mocking_strategies = {}
    
    def network_interception_basics(self, page):
        """Базовые техники перехвата сетевых запросов"""
        
        # Перехват всех запросов
        def intercept_all_requests():
            page.on("request", lambda request: print(f"Request: {request.method} {request.url}"))
            page.on("response", lambda response: print(f"Response: {response.status} {response.url}"))
        
        # Перехват конкретных запросов
        def intercept_specific_requests():
            def handle_api_request(route, request):
                if "api/users" in request.url:
                    route.fulfill(
                        status=200,
                        content_type="application/json",
                        body=json.dumps({"users": [{"id": 1, "name": "Test User"}]})
                    )
                else:
                    route.continue_()
            
            page.route("**/api/**", handle_api_request)
        
        return {
            "intercept_all": intercept_all_requests,
            "intercept_specific": intercept_specific_requests
        }
    
    def api_mocking_strategies(self, page):
        """Стратегии мокирования API"""
        
        class APIMockingStrategies:
            def mock_user_data(self, page):
                """Мокирование данных пользователя"""
                mock_users = [
                    {"id": 1, "name": "Alice", "email": "alice@example.com"},
                    {"id": 2, "name": "Bob", "email": "bob@example.com"},
                    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
                ]
                
                def mock_users_endpoint(route, request):
                    route.fulfill(
                        status=200,
                        content_type="application/json",
                        headers={"Access-Control-Allow-Origin": "*"},
                        body=json.dumps(mock_users)
                    )
                
                page.route("**/api/users", mock_users_endpoint)
            
            def mock_slow_network(self, page):
                """Симуляция медленной сети"""
                def delay_response(route, request):
                    # Добавляем задержку 2 секунды
                    page.wait_for_timeout(2000)
                    route.continue_()
                
                page.route("**/api/**", delay_response)
            
            def mock_error_responses(self, page):
                """Мокирование ошибок API"""
                def mock_500_error(route, request):
                    route.fulfill(
                        status=500,
                        content_type="application/json",
                        body=json.dumps({"error": "Internal Server Error"})
                    )
                
                page.route("**/api/critical-endpoint", mock_500_error)
        
        return APIMockingStrategies()
    
    def request_response_analysis(self, page):
        """Анализ запросов и ответов"""
        
        class NetworkAnalyzer:
            def __init__(self):
                self.requests = []
                self.responses = []
            
            def capture_network_traffic(self, page):
                """Захват всего сетевого трафика"""
                page.on("request", lambda req: self.requests.append({
                    "url": req.url,
                    "method": req.method,
                    "headers": dict(req.headers),
                    "post_data": req.post_data
                }))
                
                page.on("response", lambda res: self.responses.append({
                    "url": res.url,
                    "status": res.status,
                    "headers": dict(res.headers),
                    "timing": res.request.timing
                }))
            
            def get_failed_requests(self):
                """Получение неудачных запросов"""
                return [r for r in self.responses if r["status"] >= 400]
            
            def get_slow_requests(self, threshold_ms=1000):
                """Получение медленных запросов"""
                slow = []
                for response in self.responses:
                    timing = response.get("timing", {})
                    if timing.get("responseEnd", 0) > threshold_ms:
                        slow.append(response)
                return slow
        
        return NetworkAnalyzer()

# ПРАКТИЧЕСКИЕ ПРИМЕРЫ API ТЕСТИРОВАНИЯ:

class APIIntegrationExamples:
    def graphql_testing(self, page):
        """Тестирование GraphQL API"""
        
        def test_graphql_query(page):
            # Мокирование GraphQL ответа
            mock_graphql_response = {
                "data": {
                    "products": [
                        {"id": "1", "name": "Laptop", "price": 999.99},
                        {"id": "2", "name": "Mouse", "price": 29.99}
                    ]
                }
            }
            
            def mock_graphql_route(route, request):
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(mock_graphql_response)
                )
            
            page.route("**/graphql", mock_graphql_route)
            
            # Тестирование
            page.goto("/products")
            product_cards = page.locator(".product-card")
            expect(product_cards).to_have_count(2)
    
    def authentication_testing(self, page):
        """Тестирование аутентификации API"""
        
        def test_jwt_token_handling(page):
            # Мокирование auth endpoint
            def mock_auth_route(route, request):
                if request.post_data_json.get("username") == "admin":
                    route.fulfill(
                        status=200,
                        content_type="application/json",
                        body=json.dumps({
                            "token": "mock-jwt-token",
                            "expires_in": 3600
                        })
                    )
                else:
                    route.fulfill(
                        status=401,
                        content_type="application/json",
                        body=json.dumps({"error": "Invalid credentials"})
                    )
            
            page.route("**/auth/login", mock_auth_route)
            
            # Тест
            page.goto("/login")
            page.fill("#username", "admin")
            page.fill("#password", "password")
            page.click("#login-btn")
            
            # Проверка установки токена
            cookies = page.context.cookies()
            jwt_cookie = [c for c in cookies if c["name"] == "auth_token"]
            assert len(jwt_cookie) > 0
    
    def rate_limiting_simulation(self, page):
        """Симуляция rate limiting"""
        
        def test_rate_limiting(page):
            request_count = 0
            
            def rate_limit_route(route, request):
                nonlocal request_count
                request_count += 1
                
                if request_count > 5:  # Лимит 5 запросов
                    route.fulfill(
                        status=429,
                        content_type="application/json",
                        body=json.dumps({"error": "Rate limit exceeded"})
                    )
                else:
                    route.fulfill(
                        status=200,
                        content_type="application/json",
                        body=json.dumps({"data": f"Response {request_count}"})
                    )
            
            page.route("**/api/data", rate_limit_route)
            
            # Тест - первые 5 запросов успешны
            for i in range(5):
                page.reload()
                assert page.locator(".data-display").is_visible()
            
            # 6-й запрос должен получить ошибку
            page.reload()
            error_message = page.locator(".error-message")
            expect(error_message).to_be_visible()

# ЛУЧШИЕ ПРАКТИКИ API ТЕСТИРОВАНИЯ:
api_testing_best_practices = [
    "Всегда мокируйте внешние API в тестах",
    "Проверяйте обработку ошибок API",
    "Тестируйте различные HTTP статусы",
    "Валидируйте структуру JSON ответов",
    "Тестируйте таймауты и медленные ответы",
    "Проверяйте CORS и security headers",
    "Тестируйте аутентификацию и авторизацию"
]
```

## 📁 Работа с файлами и загрузками

### Мастерство файловых операций

```python
# ПРОДВИНУТОЕ ТЕСТИРОВАНИЕ ФАЙЛОВ И ЗАГРУЗОК

class FileOperationsTesting:
    def __init__(self):
        self.upload_strategies = {}
        self.download_handlers = {}
    
    def file_upload_testing(self, page):
        """Тестирование загрузки файлов"""
        
        class UploadTester:
            def __init__(self, page):
                self.page = page
                self.test_files_dir = Path("./test_files")
                self.test_files_dir.mkdir(exist_ok=True)
            
            def create_test_files(self):
                """Создание тестовых файлов"""
                # Текстовый файл
                text_file = self.test_files_dir / "test_document.txt"
                text_file.write_text("This is a test document content")
                
                # Изображение (имитация)
                image_file = self.test_files_dir / "test_image.jpg"
                image_file.write_bytes(b"fake_image_data")
                
                # PDF файл
                pdf_file = self.test_files_dir / "test_document.pdf"
                pdf_file.write_bytes(b"%PDF-fake-pdf-content")
                
                return [text_file, image_file, pdf_file]
            
            def test_single_file_upload(self):
                """Тест одиночной загрузки файла"""
                test_files = self.create_test_files()
                text_file = test_files[0]
                
                # Настройка контекста для загрузок
                with self.page.expect_file_chooser() as fc_info:
                    self.page.click("#upload-button")
                
                file_chooser = fc_info.value
                file_chooser.set_files(str(text_file))
                
                # Проверка результата загрузки
                self.page.wait_for_selector(".upload-success")
                uploaded_filename = self.page.locator("#uploaded-filename").text_content()
                assert uploaded_filename == text_file.name
            
            def test_multiple_file_upload(self):
                """Тест множественной загрузки"""
                test_files = self.create_test_files()
                
                # Настройка множественной загрузки
                with self.page.expect_file_chooser() as fc_info:
                    self.page.click("#multi-upload-button")
                
                file_chooser = fc_info.value
                file_chooser.set_files([str(f) for f in test_files])
                
                # Проверка загрузки всех файлов
                uploaded_list = self.page.locator(".uploaded-file-item")
                expect(uploaded_list).to_have_count(len(test_files))
            
            def test_drag_and_drop_upload(self):
                """Тест drag and drop загрузки"""
                test_files = self.create_test_files()
                text_file = test_files[0]
                
                # Симуляция drag and drop
                with self.page.expect_file_chooser() as fc_info:
                    # Триггер события drag and drop
                    self.page.dispatch_event("#drop-zone", "dragenter")
                    self.page.dispatch_event("#drop-zone", "drop")
                
                file_chooser = fc_info.value
                file_chooser.set_files(str(text_file))
                
                # Проверка
                expect(self.page.locator(".upload-complete")).to_be_visible()
        
        return UploadTester(page)
    
    def file_download_testing(self, page):
        """Тестирование скачивания файлов"""
        
        class DownloadTester:
            def __init__(self, page):
                self.page = page
                self.downloads_dir = Path("./test_downloads")
                self.downloads_dir.mkdir(exist_ok=True)
            
            def setup_download_context(self):
                """Настройка контекста для скачивания"""
                return self.page.context.new_cdp_session(self.page)
            
            def test_file_download(self):
                """Тест скачивания файла"""
                # Ожидание скачивания
                with self.page.expect_download() as download_info:
                    self.page.click("#download-link")
                
                download = download_info.value
                
                # Проверка метаданных
                assert download.suggested_filename == "report.pdf"
                assert download.url.endswith("/download/report.pdf")
                
                # Сохранение файла
                download.save_as(str(self.downloads_dir / download.suggested_filename))
                
                # Проверка содержимого
                downloaded_file = self.downloads_dir / download.suggested_filename
                assert downloaded_file.exists()
                assert downloaded_file.stat().st_size > 0
            
            def test_dynamic_content_download(self):
                """Тест скачивания динамического контента"""
                # Заполнение формы перед скачиванием
                self.page.fill("#report-type", "monthly")
                self.page.fill("#date-range", "2024-01")
                
                with self.page.expect_download() as download_info:
                    self.page.click("#generate-report")
                
                download = download_info.value
                filename = download.suggested_filename
                
                # Проверка динамического имени файла
                assert "monthly" in filename
                assert "2024-01" in filename
                assert filename.endswith(".xlsx")
        
        return DownloadTester(page)
    
    def file_validation_testing(self, page):
        """Тестирование валидации файлов"""
        
        def test_file_type_validation(page):
            """Тест валидации типов файлов"""
            
            # Создание файла неправильного типа
            wrong_file = Path("./test_files/script.exe")
            wrong_file.write_bytes(b"malicious_content")
            
            # Попытка загрузки
            with page.expect_file_chooser() as fc_info:
                page.click("#image-upload")
            
            file_chooser = fc_info.value
            file_chooser.set_files(str(wrong_file))
            
            # Проверка ошибки валидации
            error_message = page.locator(".file-validation-error")
            expect(error_message).to_be_visible()
            expect(error_message).to_contain_text("Invalid file type")
        
        def test_file_size_validation(page):
            """Тест валидации размера файлов"""
            
            # Создание большого файла
            large_file = Path("./test_files/large_document.pdf")
            large_file.write_bytes(b"x" * (10 * 1024 * 1024))  # 10MB
            
            with page.expect_file_chooser() as fc_info:
                page.click("#document-upload")
            
            file_chooser = fc_info.value
            file_chooser.set_files(str(large_file))
            
            # Проверка ошибки размера
            size_error = page.locator(".size-limit-error")
            expect(size_error).to_be_visible()
            expect(size_error).to_contain_text("File too large")

# ЛУЧШИЕ ПРАКТИКИ ФАЙЛОВЫХ ОПЕРАЦИЙ:
file_testing_best_practices = [
    "Всегда очищайте тестовые файлы после тестов",
    "Используйте уникальные имена для тестовых файлов",
    "Проверяйте MIME типы и расширения файлов",
    "Тестируйте ограничения размера файлов",
    "Проверяйте обработку ошибок загрузки",
    "Тестируйте прогресс-бары и статусы загрузки",
    "Проверяйте безопасность загрузки файлов"
]
```

## 📱 Мобильное и адаптивное тестирование

### Тестирование на разных устройствах

```python
# МОБИЛЬНОЕ И АДАПТИВНОЕ ТЕСТИРОВАНИЕ

class MobileTesting:
    def __init__(self):
        self.device_presets = {}
        self.responsive_strategies = {}
    
    def device_emulation(self, playwright):
        """Эмуляция мобильных устройств"""
        
        class DeviceEmulator:
            def __init__(self, playwright):
                self.playwright = playwright
            
            def get_device_descriptors(self):
                """Получение доступных девайсов"""
                devices = self.playwright.devices
                mobile_devices = {
                    name: config for name, config in devices.items()
                    if any(keyword in name.lower() for keyword in ['iphone', 'pixel', 'galaxy'])
                }
                return mobile_devices
            
            def create_mobile_context(self, device_name="iPhone 12"):
                """Создание контекста для мобильного устройства"""
                device = self.playwright.devices[device_name]
                
                context = self.playwright.chromium.launchPersistentContext(
                    "",
                    **device,
                    locale="ru-RU",
                    timezone_id="Europe/Moscow",
                    permissions=["geolocation"]
                )
                
                return context
            
            def test_responsive_design(self, page, breakpoints=None):
                """Тестирование адаптивного дизайна"""
                if breakpoints is None:
                    breakpoints = [
                        {"width": 320, "height": 568, "name": "Mobile S"},
                        {"width": 768, "height": 1024, "name": "Tablet"},
                        {"width": 1024, "height": 768, "name": "Desktop S"},
                        {"width": 1920, "height": 1080, "name": "Desktop L"}
                    ]
                
                results = []
                
                for bp in breakpoints:
                    # Изменение размера viewport
                    page.set_viewport_size({"width": bp["width"], "height": bp["height"]})
                    page.reload()
                    
                    # Проверки для каждого breakpoint
                    checks = {
                        "viewport": f"{bp['width']}x{bp['height']}",
                        "device": bp["name"],
                        "menu_visibility": self.check_mobile_menu_visibility(page),
                        "content_layout": self.check_content_adaptation(page),
                        "touch_elements": self.check_touch_target_sizes(page),
                        "scroll_behavior": self.check_scroll_performance(page)
                    }
                    
                    results.append(checks)
                
                return results
            
            def check_mobile_menu_visibility(self, page):
                """Проверка видимости мобильного меню"""
                hamburger_menu = page.locator(".mobile-menu-toggle")
                main_nav = page.locator(".main-navigation")
                
                if page.viewport_size["width"] < 768:
                    return hamburger_menu.is_visible() and not main_nav.is_visible()
                else:
                    return not hamburger_menu.is_visible() and main_nav.is_visible()
            
            def check_content_adaptation(self, page):
                """Проверка адаптации контента"""
                content_width = page.evaluate("""() => {
                    const content = document.querySelector('.main-content');
                    return content ? content.offsetWidth : 0;
                }""")
                
                viewport_width = page.viewport_size["width"]
                
                # Контент не должен быть шире viewport
                return content_width <= viewport_width
            
            def check_touch_target_sizes(self, page):
                """Проверка размеров touch targets"""
                small_buttons = page.locator("button, a, input").filter(
                    lambda element: element.bounding_box()["width"] < 44 or 
                                   element.bounding_box()["height"] < 44
                )
                
                return small_buttons.count() == 0  # Нет слишком маленьких элементов
        
        return DeviceEmulator(playwright)
    
    def touch_interaction_testing(self, page):
        """Тестирование touch взаимодействий"""
        
        class TouchTester:
            def __init__(self, page):
                self.page = page
            
            def test_gesture_recognition(self):
                """Тест распознавания жестов"""
                
                # Swipe left gesture
                def swipe_left(element_selector):
                    element = self.page.locator(element_selector)
                    box = element.bounding_box()
                    
                    # Симуляция swipe жеста
                    self.page.touchscreen.tap(box["x"] + box["width"] - 10, box["y"] + box["height"]/2)
                    self.page.touchscreen.move(box["x"] + 10, box["y"] + box["height"]/2)
                    self.page.touchscreen.up()
                
                # Pinch to zoom
                def pinch_zoom():
                    # Симуляция pinch жеста
                    self.page.touchscreen.tap(100, 100)
                    self.page.touchscreen.tap(200, 200)
                    # Zoom logic here
                    
                # Тестирование
                swipe_left(".carousel-item")
                expect(self.page.locator(".carousel-item.active")).to_have_count(1)
            
            def test_long_press(self):
                """Тест долгого нажатия"""
                context_menu = self.page.locator(".context-menu")
                
                # Долгое нажатие
                self.page.locator(".selectable-item").click(delay=1000)
                
                # Проверка появления контекстного меню
                expect(context_menu).to_be_visible()
            
            def test_multi_touch(self):
                """Тест мультитач взаимодействий"""
                # Симуляция двух пальцев
                self.page.touchscreen.tap(100, 100)
                self.page.touchscreen.tap(200, 200)
                
                # Проверка реакции на multitouch
                zoom_level = self.page.evaluate("() => window.zoomLevel || 1")
                assert zoom_level != 1  # Должно измениться
            
            def test_keyboard_avoidance(self):
                """Тест избегания клавиатуры"""
                # Фокус на поле ввода
                input_field = self.page.locator("#message-input")
                input_field.click()
                
                # Проверка что элементы сдвигаются вверх
                initial_position = input_field.bounding_box()["y"]
                
                # Ввод текста (вызывает появление клавиатуры)
                input_field.type("Test message")
                
                # Проверка сдвига
                final_position = input_field.bounding_box()["y"]
                assert final_position < initial_position  # Элемент поднялся
        
        return TouchTester(page)
    
    def orientation_testing(self, page):
        """Тестирование смены ориентации"""
        
        def test_orientation_changes(page):
            """Тест смены портретной/ландшафтной ориентации"""
            
            # Начальная портретная ориентация
            page.set_viewport_size({"width": 375, "height": 667})  # iPhone portrait
            page.goto("/")
            
            # Проверка портретного режима
            portrait_checks = {
                "menu_collapsed": page.locator(".mobile-menu").is_visible(),
                "content_vertical": page.locator(".content-column").count() == 1
            }
            
            # Смена на ландшафт
            page.set_viewport_size({"width": 667, "height": 375})  # iPhone landscape
            page.reload()
            
            # Проверка ландшафтного режима
            landscape_checks = {
                "menu_expanded": page.locator(".desktop-menu").is_visible(),
                "content_horizontal": page.locator(".content-column").count() > 1
            }
            
            return {
                "portrait": portrait_checks,
                "landscape": landscape_checks
            }

# ЛУЧШИЕ ПРАКТИКИ МОБИЛЬНОГО ТЕСТИРОВАНИЯ:
mobile_testing_best_practices = [
    "Тестируйте на реальных устройствах, а не только эмуляторах",
    "Проверяйте performance на слабых устройствах",
    "Тестируйте разные ориентации экрана",
    "Проверяйте адаптацию под notch и status bar",
    "Тестируйте offline режимы",
    "Проверяйте работу с медленным интернетом",
    "Тестируйте accessibility на мобильных устройствах"
]
```

## 👁️ Visual Testing

### Сравнение скриншотов и визуальная регрессия

```python
# VISUAL TESTING И СКРИНШОТЫ

class VisualTesting:
    def __init__(self):
        self.screenshot_strategies = {}
        self.comparison_methods = {}
    
    def screenshot_capture_strategies(self, page):
        """Стратегии захвата скриншотов"""
        
        class ScreenshotManager:
            def __init__(self, page):
                self.page = page
                self.screenshots_dir = Path("./screenshots")
                self.screenshots_dir.mkdir(exist_ok=True)
            
            def capture_full_page_screenshot(self, name):
                """Полностраничный скриншот"""
                filename = self.screenshots_dir / f"{name}_full.png"
                self.page.screenshot(
                    path=str(filename),
                    full_page=True,
                    quality=80
                )
                return filename
            
            def capture_element_screenshot(self, selector, name):
                """Скриншот конкретного элемента"""
                element = self.page.locator(selector)
                filename = self.screenshots_dir / f"{name}_element.png"
                
                element.screenshot(
                    path=str(filename),
                    omit_background=True
                )
                return filename
            
            def capture_viewport_screenshot(self, name):
                """Скриншот текущего viewport"""
                filename = self.screenshots_dir / f"{name}_viewport.png"
                self.page.screenshot(
                    path=str(filename),
                    clip={
                        "x": 0,
                        "y": 0,
                        "width": self.page.viewport_size["width"],
                        "height": self.page.viewport_size["height"]
                    }
                )
                return filename
            
            def capture_screenshots_across_breakpoints(self, name, breakpoints=None):
                """Скриншоты на разных breakpoint'ах"""
                if breakpoints is None:
                    breakpoints = [
                        {"width": 375, "height": 667, "name": "mobile"},
                        {"width": 768, "height": 1024, "name": "tablet"},
                        {"width": 1200, "height": 800, "name": "desktop"}
                    ]
                
                screenshots = {}
                
                for bp in breakpoints:
                    self.page.set_viewport_size({
                        "width": bp["width"],
                        "height": bp["height"]
                    })
                    self.page.reload()
                    
                    filename = self.capture_full_page_screenshot(
                        f"{name}_{bp['name']}_{bp['width']}x{bp['height']}"
                    )
                    screenshots[bp["name"]] = str(filename)
                
                return screenshots
        
        return ScreenshotManager(page)
    
    def visual_regression_testing(self):
        """Тестирование визуальной регрессии"""
        
        class VisualRegressionTester:
            def __init__(self):
                self.baseline_dir = Path("./baseline_screenshots")
                self.current_dir = Path("./current_screenshots")
                self.diffs_dir = Path("./diff_screenshots")
                
                # Создание директорий
                for directory in [self.baseline_dir, self.current_dir, self.diffs_dir]:
                    directory.mkdir(exist_ok=True)
            
            def create_baseline(self, page, test_name):
                """Создание baseline скриншотов"""
                filename = self.baseline_dir / f"{test_name}.png"
                page.screenshot(path=str(filename), full_page=True)
                return str(filename)
            
            def compare_with_baseline(self, page, test_name, threshold=0.1):
                """Сравнение с baseline"""
                import cv2
                import numpy as np
                
                # Создание текущего скриншота
                current_file = self.current_dir / f"{test_name}.png"
                page.screenshot(path=str(current_file), full_page=True)
                
                # Загрузка изображений
                baseline_img = cv2.imread(str(self.baseline_dir / f"{test_name}.png"))
                current_img = cv2.imread(str(current_file))
                
                if baseline_img is None:
                    raise FileNotFoundError(f"Baseline screenshot not found for {test_name}")
                
                # Изменение размера если нужно
                if baseline_img.shape != current_img.shape:
                    current_img = cv2.resize(current_img, (baseline_img.shape[1], baseline_img.shape[0]))
                
                # Сравнение
                diff = cv2.absdiff(baseline_img, current_img)
                diff_percentage = np.sum(diff) / np.sum(baseline_img)
                
                # Создание diff изображения
                if diff_percentage > 0:
                    diff_file = self.diffs_dir / f"{test_name}_diff.png"
                    cv2.imwrite(str(diff_file), diff)
                
                return {
                    "difference_percentage": diff_percentage,
                    "is_different": diff_percentage > threshold,
                    "threshold": threshold
                }
            
            def pixel_perfect_comparison(self, page, test_name):
                """Pixel-perfect сравнение"""
                comparison = self.compare_with_baseline(page, test_name, threshold=0.0)
                return comparison["is_different"]  # True если есть хоть 1 пиксель разницы
            
            def ignore_regions_comparison(self, page, test_name, ignore_regions=None):
                """Сравнение с игнорированием регионов"""
                if ignore_regions is None:
                    ignore_regions = [
                        {"selector": ".dynamic-content"},  # Игнорировать динамический контент
                        {"selector": ".timestamp"},         # Игнорировать временные метки
                        {"selector": ".user-avatar"}        # Игнорировать аватары
                    ]
                
                # Создание маски для игнорируемых регионов
                mask = self.create_ignore_mask(page, ignore_regions)
                
                # Сравнение с маской
                # (реализация зависит от используемой библиотеки сравнения)
        
        return VisualRegressionTester()
    
    def create_ignore_mask(self, page, ignore_regions):
        """Создание маски для игнорирования регионов"""
        import numpy as np
        
        # Получение размеров страницы
        page_width = page.evaluate("() => document.body.scrollWidth")
        page_height = page.evaluate("() => document.body.scrollHeight")
        
        # Создание черной маски
        mask = np.zeros((page_height, page_width), dtype=np.uint8)
        
        # Заполнение белым цветом игнорируемых регионов
        for region in ignore_regions:
            if "selector" in region:
                try:
                    element = page.locator(region["selector"])
                    if element.is_visible():
                        bbox = element.bounding_box()
                        if bbox:
                            x, y = int(bbox["x"]), int(bbox["y"])
                            w, h = int(bbox["width"]), int(bbox["height"])
                            mask[y:y+h, x:x+w] = 255  # Белый - игнорировать
                except:
                    continue  # Игнорировать ошибки поиска элементов
        
        return mask

# ПРАКТИЧЕСКИЕ ПРИМЕРЫ VISUAL TESTING:

class VisualTestingExamples:
    def test_brand_consistency(self, page):
        """Тест консистентности бренда"""
        
        def check_color_scheme_consistency(page):
            """Проверка цветовой схемы"""
            
            # Проверка основных цветов
            brand_colors = page.evaluate("""() => {
                const styles = getComputedStyle(document.documentElement);
                return {
                    primary: styles.getPropertyValue('--primary-color'),
                    secondary: styles.getPropertyValue('--secondary-color'),
                    accent: styles.getPropertyValue('--accent-color')
                };
            }""")
            
            expected_colors = {
                "primary": "#007bff",
                "secondary": "#6c757d", 
                "accent": "#28a745"
            }
            
            for color_name, expected_value in expected_colors.items():
                assert brand_colors[color_name] == expected_value, \
                    f"Inconsistent {color_name}: expected {expected_value}, got {brand_colors[color_name]}"
        
        def check_typography_consistency(page):
            """Проверка типографики"""
            # Проверка размеров шрифтов
            font_sizes = page.evaluate("""() => {
                const headings = document.querySelectorAll('h1, h2, h3');
                return Array.from(headings).map(h => ({
                    tag: h.tagName,
                    fontSize: getComputedStyle(h).fontSize
                }));
            }""")
            
            expected_sizes = {
                "H1": "32px",
                "H2": "24px", 
                "H3": "20px"
            }
            
            for heading in font_sizes:
                expected_size = expected_sizes.get(heading["tag"])
                assert heading["fontSize"] == expected_size, \
                    f"Inconsistent font size for {heading['tag']}"
    
    def test_layout_stability(self, page):
        """Тест стабильности лAYOUT"""
        
        def check_element_positions(page):
            """Проверка стабильности позиций элементов"""
            
            # Сохранение позиций элементов
            baseline_positions = {}
            elements_to_track = [".header", ".main-nav", ".hero-section", ".footer"]
            
            for selector in elements_to_track:
                element = page.locator(selector)
                if element.is_visible():
                    bbox = element.bounding_box()
                    baseline_positions[selector] = {
                        "x": bbox["x"],
                        "y": bbox["y"],
                        "width": bbox["width"],
                        "height": bbox["height"]
                    }
            
            # После некоторых действий - проверка позиций
            page.click("#some-action")
            page.wait_for_timeout(1000)  # Дать время на обновление
            
            for selector, baseline_pos in baseline_positions.items():
                element = page.locator(selector)
                if element.is_visible():
                    current_bbox = element.bounding_box()
                    # Проверка что позиции не изменились значительно
                    assert abs(current_bbox["x"] - baseline_pos["x"]) < 5
                    assert abs(current_bbox["y"] - baseline_pos["y"]) < 5

# ЛУЧШИЕ ПРАКТИКИ VISUAL TESTING:
visual_testing_best_practices = [
    "Создавайте baseline скриншоты на стабильной версии",
    "Игнорируйте динамический контент в сравнениях",
    "Используйте подходящие threshold значения",
    "Тестируйте на разных устройствах и браузерах",
    "Храните baseline скриншоты в системе контроля версий",
    "Автоматизируйте visual testing в CI/CD",
    "Проверяйте accessibility контрастности цветов"
]
```

## ❓ Ответы на вопросы студентов

### Продвинутые технические вопросы

**Q: Как обрабатывать flaky тесты в Playwright?**

A:
```python
# ОБРАБОТКА FLAKY ТЕСТОВ

class FlakyTestHandler:
    def __init__(self):
        self.retry_strategies = {}
    
    def automatic_retry_mechanism(self):
        """Автоматический механизм повторных попыток"""
        
        import pytest
        
        @pytest.mark.flaky(reruns=3, reruns_delay=2)
        def test_that_might_fail(page):
            """Тест с автоматическим retry"""
            # Этот тест будет автоматически повторен до 3 раз
            # с задержкой 2 секунды между попытками
            page.goto("https://flaky-example.com")
            expect(page.locator("#critical-element")).to_be_visible()
    
    def custom_retry_logic(self, page):
        """Пользовательская логика retry"""
        
        def retry_until_success(operation, max_attempts=3, delay=1000):
            """Retry до успеха"""
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    result = operation()
                    return result  # Успех - возвращаем результат
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"Attempt {attempt + 1} failed, retrying...")
                        page.wait_for_timeout(delay)
                    else:
                        print(f"All {max_attempts} attempts failed")
            
            # Если все попытки провалились
            raise last_exception
        
        # Использование
        def flaky_operation():
            element = page.locator("#sometimes-missing-element")
            if not element.is_visible():
                raise Exception("Element not visible")
            return element.text_content()
        
        # Выполнение с retry
        result = retry_until_success(flaky_operation)
    
    def conditional_retry(self, page):
        """Условный retry на основе типа ошибки"""
        
        def smart_retry(operation):
            """Retry только для определенных типов ошибок"""
            max_attempts = 3
            
            for attempt in range(max_attempts):
                try:
                    return operation()
                except TimeoutError:
                    # Retry для timeout ошибок
                    if attempt < max_attempts - 1:
                        page.reload()
                        page.wait_for_timeout(2000)
                        continue
                    raise
                except AssertionError:
                    # Не retry для assertion ошибок
                    raise
                except Exception as e:
                    # Retry для других ошибок
                    if "network" in str(e).lower() or "connection" in str(e).lower():
                        if attempt < max_attempts - 1:
                            page.wait_for_timeout(3000)
                            continue
                    raise
    
    def flaky_test_patterns(self):
        """Паттерны для обработки flaky тестов"""
        
        patterns = {
            "wait_for_stability": {
                "description": "Ожидание стабильного состояния",
                "example": """
                # Вместо:
                page.click("#button")
                expect(page.locator("#result")).to_be_visible()
                
                # Используйте:
                page.click("#button")
                page.locator("#result").wait_for(state="visible", timeout=10000)
                """
            },
            
            "explicit_waits": {
                "description": "Явные ожидания вместо sleep",
                "example": """
                # Плохо:
                time.sleep(2)
                element.click()
                
                # Хорошо:
                element.wait_for(state="enabled")
                element.click()
                """
            },
            
            "network_stability": {
                "description": "Ожидание стабильной сети",
                "example": """
                # Ожидание завершения всех сетевых запросов
                page.wait_for_load_state("networkidle")
                """
            }
        }
        
        return patterns

# ЛУЧШИЕ ПРАКТИКИ ДЛЯ FLAKY ТЕСТОВ:
flaky_test_best_practices = [
    "Используйте встроенные wait механизмы Playwright",
    "Избегайте sleep(), используйте явные ожидания",
    "Применяйте retry только для нестабильных операций",
    "Логгируйте попытки retry для анализа",
    "Изолируйте тестовые данные и состояния",
    "Используйте fresh browser context для каждого теста",
    "Проверяйте тесты на разных средах"
]
```

## 📋 Подробный тайминг занятий

### Занятие 5.1: Расширенное API тестирование (90 минут)

**0-10 мин: Введение в продвинутое тестирование**
- Обзор целей модуля
- Сравнение с базовым тестированием
- **Демонстрация сложных сценариев**

**10-35 мин: Теория - Продвинутые API техники**
- Network interception и mocking
- GraphQL и REST API тестирование
- Authentication и security testing
- **Живые демонстрации перехвата запросов**

**35-60 мин: Практика - Complex API scenarios**
- Создание mock серверов
- Тестирование rate limiting
- Обработка ошибок API
- **Интерактивное кодирование с преподавателем**

**60-75 мин: Самостоятельная практика**
- Студенты создают свои API тесты
- Работа с реальными API endpoints
- **Индивидуальная помощь преподавателя**

**75-90 мин: Закрепление и домашнее задание**
- Разбор сложных случаев
- Ответы на вопросы
- Назначение домашнего задания
- **Анонс следующего занятия**

---
*Модуль 5 развивает навыки до уровня senior автоматизатора*