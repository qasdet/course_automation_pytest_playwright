# 05 — E2E тестирование: сценарии и архитектура

Цели:

- Построить E2E тест, покрывающий реальный пользовательский сценарий
- Организовать тесты, фикстуры и вспомогательные модули
- Научиться параллелить тесты и собирать отчёты

Структура E2E проекта

- `tests/` — тесты
- `pages/` — Page Object Model (POM) классы
- `fixtures/` — фикстуры для запуска тестовой среды

Пример простой POM (файл `pages/example_page.py`):

```python
class ExamplePage:
    def __init__(self, page):
        self.page = page
        self.header = page.locator('h1')

    def goto(self):
        self.page.goto('https://example.com')

    def get_header(self):
        return self.header.inner_text()
```

Пример теста с POM (`tests/test_flow.py`):

```python
from pages.example_page import ExamplePage

def test_flow(page):
    p = ExamplePage(page)
    p.goto()
    assert p.get_header() == 'Example Domain'
```

Практическое задание:

1. Реализуйте POM для `example.com` и напишите один сценарий пользователя.
2. Настройте запуск тестов параллельно: `pytest -n auto` (через `pytest-xdist`).
3. Соберите отчёт в `junitxml`: `pytest --junitxml=report.xml`.
