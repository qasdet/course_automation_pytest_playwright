# 04 — Введение в Playwright (Python)

Цели:

- Понять архитектуру Playwright и его преимущества
- Научиться запускать браузер, навигировать по странице и делать селекторы
- Написать простой тест открытия страницы и проверки содержимого

Установка и подготовка

```bash
pip install playwright
playwright install
```

Простой пример (синхронный вариант через Playwright sync API):

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')
    assert 'Example Domain' in page.title()
    browser.close()
```

Playwright + pytest

Установите `pytest-playwright` и используйте фикстуры `page`/`browser`.

Пример теста `tests/test_example.py`:

```python
def test_example(page):
    page.goto('https://example.com')
    assert page.locator('h1').inner_text() == 'Example Domain'
```

Практическое задание:

1. Напишите тест, который открывает `https://example.com`, кликает по ссылке "More information..." и проверяет редирект.
2. Попробуйте запустить тесты в headless и headed режимах.

Советы:

- Селекторы: используйте `page.locator()` и отказываться от XPath при возможности.
- Таймауты: задавайте разумные таймауты и используйте `page.wait_for_*` методы.
