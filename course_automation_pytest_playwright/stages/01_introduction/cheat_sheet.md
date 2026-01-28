# 🚀 Шпаргалка по командам и инструментам

## 🐍 Python команды

### Основные команды
```bash
# Проверка версии Python
python --version
python3 --version

# Запуск Python интерпретатора
python
python3

# Выполнение Python скрипта
python script.py
python3 my_script.py

# Установка пакетов
pip install package_name
pip install package_name==1.2.3  # конкретная версия

# Обновление pip
python -m pip install --upgrade pip

# Просмотр установленных пакетов
pip list
pip freeze

# Сохранение зависимостей
pip freeze > requirements.txt

# Установка из requirements.txt
pip install -r requirements.txt
```

### Виртуальное окружение
```bash
# Создание виртуального окружения
python -m venv .venv
python3 -m venv my_env

# Активация (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Активация (Windows Command Prompt)
.venv\Scripts\activate.bat

# Активация (Linux/Mac)
source .venv/bin/activate

# Деактивация
deactivate

# Удаление окружения
# Просто удалите папку .venv
```

## 🧪 pytest команды

### Базовые команды
```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск одного файла
pytest test_file.py

# Запуск конкретного теста
pytest test_file.py::test_function_name

# Запуск тестов по маркеру
pytest -m marker_name

# Запуск с остановкой при первой ошибке
pytest -x

# Запуск последних неудачных тестов
pytest --lf

# Запуск тестов с повтором при падении
pytest --reruns 3
```

### Полезные флаги
```bash
# Подробный вывод
pytest -v

# Очень подробный вывод
pytest -vv

# Тихий режим
pytest -q

# Показать локальные переменные при падении
pytest --tb=long

# Запуск в случайном порядке
pytest --random-order

# Параллельный запуск
pytest -n 4  # 4 процесса

# Генерация отчета в HTML
pytest --html=report.html

# Покрытие кода
pytest --cov=package_name
pytest --cov=src --cov-report=html
```

### Маркеры и выборка
```bash
# Запуск тестов по имени
pytest -k "test_login"

# Запуск тестов по выражению
pytest -k "test_login or test_logout"

# Исключение тестов
pytest -k "not slow"

# Запуск тестов с конкретным маркером
pytest -m smoke
pytest -m "not slow"

# Список всех маркеров
pytest --markers
```

## 🌐 Playwright команды

### Установка и настройка
```bash
# Установка Playwright
pip install playwright

# Установка браузеров
playwright install
playwright install chromium firefox webkit

# Установка с системными зависимостями
playwright install --with-deps

# Проверка установки
playwright --version
```

### Запуск тестов
```bash
# Запуск тестов с Playwright
pytest --headed  # с видимым браузером
pytest --browser chromium  # конкретный браузер
pytest --slowmo 1000  # замедление на 1 секунду

# Генерация отчетов
pytest --video=retain-on-failure
pytest --screenshot=only-on-failure
pytest --trace  # трассировка для отладки
```

### Инструменты Playwright
```bash
# Codegen - генерация кода
playwright codegen https://example.com

# Inspector - отладка
playwright test --debug

# Open - открытие трассировки
playwright show-trace trace.zip

# Screenshot - создание скриншотов
playwright screenshot --device="iPhone 11" https://example.com example.png
```

## 🐳 Docker команды

### Основные команды
```bash
# Сборка образа
docker build -t my-image .

# Запуск контейнера
docker run my-image
docker run -it my-image bash  # интерактивный режим

# Запуск с монтированием
docker run -v $(pwd):/app my-image

# Просмотр запущенных контейнеров
docker ps
docker ps -a  # все контейнеры

# Остановка контейнера
docker stop container_name
docker kill container_name

# Удаление контейнера
docker rm container_name

# Просмотр образов
docker images

# Удаление образа
docker rmi image_name
```

### Работа с volumes и networks
```bash
# Создание volume
docker volume create my-volume

# Создание сети
docker network create my-network

# Запуск с volume
docker run -v my-volume:/data my-image

# Запуск в сети
docker run --network my-network my-image
```

## 🛠️ Git команды

### Основные операции
```bash
# Клонирование репозитория
git clone https://github.com/user/repo.git

# Проверка статуса
git status

# Добавление файлов
git add filename
git add .  # все файлы

# Создание коммита
git commit -m "Описание изменений"

# Отправка в удаленный репозиторий
git push origin main

# Получение изменений
git pull origin main

# Создание новой ветки
git checkout -b new-feature

# Переключение между ветками
git checkout branch-name
```

### Просмотр истории
```bash
# Просмотр истории коммитов
git log
git log --oneline

# Просмотр изменений
git diff
git diff --staged

# Просмотр конкретного коммита
git show commit-hash
```

## 📊 CI/CD (GitLab CI)

### Основные команды
```bash
# Локальное тестирование GitLab CI
# Установка GitLab Runner
gitlab-runner exec docker job_name

# Проверка конфигурации
# Файл .gitlab-ci.yml должен быть в корне репозитория
```

## 🔧 Отладка и диагностика

### Python отладка
```bash
# Запуск с отладчиком
python -m pdb script.py

# Интерактивная отладка
import pdb; pdb.set_trace()  # в коде

# Использование breakpoint()
breakpoint()  # Python 3.7+
```

### Логирование
```python
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Использование
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## 📦 Управление зависимостями

### pip-tools
```bash
# Установка pip-tools
pip install pip-tools

# Создание requirements.txt из requirements.in
pip-compile requirements.in

# Обновление зависимостей
pip-compile --upgrade requirements.in

# Синхронизация окружения
pip-sync
```

### Poetry (альтернатива)
```bash
# Инициализация проекта
poetry init

# Установка зависимостей
poetry install

# Добавление пакета
poetry add package_name

# Запуск команд в виртуальном окружении
poetry run pytest
```

## ⚡ Быстрые решения

### Частые задачи одной командой:

```bash
# Полная настройка нового проекта
python -m venv .venv && source .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

# Быстрая проверка тестов
pytest -x --tb=short

# Запуск с генерацией отчета
pytest --html=report.html --self-contained-html

# Отладка Playwright теста
pytest test_file.py::test_name --headed --debug

# Очистка Docker
docker system prune -a

# Быстрая диагностика Python окружения
python -c "import sys; print(sys.version); import site; print(site.getsitepackages())"
```

## 🎯 Горячие клавиши в IDE

### VS Code:
- `Ctrl+Shift+P` - Палитра команд
- `F5` - Запуск отладки
- `Ctrl+F5` - Запуск без отладки
- `Ctrl+Shift+T` - Открыть терминал
- `Ctrl+Shift+X` - Расширения

### PyCharm:
- `Shift+F10` - Запуск
- `Ctrl+Shift+F10` - Запуск контекста
- `Shift+Alt+F10` - Выбор конфигурации запуска
- `Ctrl+Shift+A` - Поиск действия

---

**💡 Совет:** Создайте alias или скрипты для часто используемых команд!