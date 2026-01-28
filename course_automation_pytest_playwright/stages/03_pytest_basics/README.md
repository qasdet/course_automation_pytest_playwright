# 03 — pytest: основы и лучшие практики

Цели:

- Познакомиться с `pytest` — структура теста, ассерты, фикстуры
- Научиться писать unit тесты и запускать их
- Разобрать маркировку тестов и запуск конкретных наборов

Теория и справка:

- Тесты пишутся в файлах `test_*.py` или `*_test.py`.
- Каждая тестовая функция должна быть независимой.
- Фикстуры (`@pytest.fixture`) позволяют подготовить окружение для теста и переиспользовать код.
- Используйте `pytest -q` для краткого вывода и `pytest -k <expr>` для отбора.

Пример простого теста (файл `tests/test_math.py`):

```python
# tests/test_math.py
import pytest

def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2
```

Фикстуры пример (`tests/conftest.py`):

```python
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_sample(sample_list):
    assert sum(sample_list) == 6
```

Практические задания:

1. Напишите тесты для функции `is_prime(n)` (сохраните в `tests/test_prime.py`).
2. Создайте фикстуру, которая создаёт временный файл и проверьте чтение/запись.
3. Добавьте в тесты метки: `@pytest.mark.slow` для долгих и `@pytest.mark.fast` для быстрых.

Советы:

- Не проверяйте внешние сервисы в unit тестах — мокайте их.
- Для асинхронных функций используйте `pytest-asyncio`.

Файлы примеров:
- `tests/test_math.py`
- `tests/test_prime.py` (создайте)
- `tests/conftest.py`
