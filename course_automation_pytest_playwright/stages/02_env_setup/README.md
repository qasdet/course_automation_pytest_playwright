# 02 — Настройка окружения

Цели:

- Поймёте как настроить виртуальное окружение
- Установите зависимости и Playwright браузеры
- Подготовите Docker образ для локального запуска тестов

Шаги (пошагово):

1. Создать и активировать virtualenv:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Unix
source .venv/bin/activate
```

2. Установить зависимости:

```bash
pip install -U pip
pip install -r requirements.txt
```

3. Установить браузеры Playwright:

```bash
playwright install
```

4. Проверить установку запустив пример из `03_pytest_basics`.

Практическое задание:

- Выполните шаги 1–3 и зафиксируйте выводы в `env_check.md`.
- Попробуйте запустить контейнер по `Dockerfile` (локально) и проверьте, что `playwright` доступен.

Советы и решения проблем:

- Если на Windows при установке Playwright возникают ошибки, используйте WSL2 или Docker образ.
- При проблемах с зависимостями попробуйте установить system‑пакеты (libnss3 и пр.) — приведены в `Dockerfile`.
