# 🛠️ Руководство по устранению неполадок (Troubleshooting Guide)

## 🔧 Общие проблемы и решения

### Проблемы с Python

#### **Ошибка: "python is not recognized as an internal or external command"**
**Решение:**
1. Проверьте, установлен ли Python: `where python` (Windows) или `which python` (Linux/Mac)
2. Добавьте Python в PATH переменную окружения
3. Переустановите Python, выбрав "Add Python to PATH" во время установки
4. Используйте `python3` вместо `python` на некоторых системах

#### **Ошибка: "No module named pip"**
**Решение:**
```bash
# Переустановка pip
python -m ensurepip --upgrade
# или
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

#### **Ошибка: "Permission denied" при установке пакетов**
**Решение:**
```bash
# Используйте флаг --user
pip install --user package_name

# Или запустите от имени администратора (не рекомендуется)
# Windows: запустите PowerShell от имени администратора
# Linux/Mac: используйте sudo (крайне не рекомендуется для pip)
```

### Проблемы с виртуальным окружением

#### **Ошибка при создании venv: "The virtual environment was not created successfully"**
**Решение:**
```bash
# Используйте полный путь к Python
python -m venv .venv

# На старых версиях Windows
python -m venv .venv --without-pip
# Затем установите pip вручную

# Альтернативный способ
pip install virtualenv
virtualenv .venv
```

#### **Ошибка активации: "Activate.ps1 cannot be loaded" (Windows)**
**Решение:**
```powershell
# Измените политику выполнения PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Или используйте cmd вместо PowerShell
.venv\Scripts\activate.bat
```

#### **Окружение активируется, но пакеты не видны**
**Решение:**
1. Убедитесь, что вы активировали правильное окружение
2. Проверьте, что pip использует правильное окружение:
   ```bash
   which pip  # Linux/Mac
   where pip  # Windows
   ```
3. Переустановите пакеты в активированном окружении

### Проблемы с установкой зависимостей

#### **Ошибка: "Could not find a version that satisfies the requirement"**
**Решение:**
```bash
# Обновите pip
pip install --upgrade pip

# Проверьте совместимость версий Python
pip debug --verbose

# Используйте конкретные версии
pip install package_name==specific_version
```

#### **Конфликты зависимостей**
**Решение:**
```bash
# Используйте pip-tools для управления зависимостями
pip install pip-tools
pip-compile requirements.in
pip-sync

# Или создайте чистое окружение
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Проблемы с Playwright

#### **Ошибка: "playwright: command not found"**
**Решение:**
```bash
# Установите Playwright
pip install playwright
# Затем установите браузеры
playwright install

# Если проблема сохраняется, попробуйте:
python -m playwright install
```

#### **Ошибка при установке браузеров: "Failed to install browsers"**
**Решение:**
```bash
# Установка с дополнительными зависимостями
playwright install --with-deps

# На Linux может потребоваться установить системные зависимости:
sudo apt-get update
sudo apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libxss1 libxcomposite1 libxrandr2 libgbm1 \
    libasound2 libpangocairo-1.0-0 libgtk-3-0

# На Windows используйте WSL2 или Docker
```

#### **Браузеры не запускаются**
**Решение:**
```python
# В коде используйте headless=False для отладки
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Видимый браузер
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()
```

### Проблемы с pytest

#### **Тесты не находятся**
**Решение:**
1. Убедитесь, что файлы названы правильно: `test_*.py` или `*_test.py`
2. Проверьте, что тесты находятся в правильной директории
3. Используйте явный путь:
   ```bash
   pytest path/to/tests/
   ```

#### **Ошибка: "fixture 'page' not found"**
**Решение:**
```bash
# Установите pytest-playwright
pip install pytest-playwright

# Или импортируйте фикстуру правильно
import pytest
from playwright.sync_api import Page

def test_example(page: Page):
    page.goto("https://example.com")
    assert "Example" in page.title()
```

#### **Тесты падают с timeout**
**Решение:**
```python
# Увеличьте таймауты
import pytest

@pytest.fixture
def page(page):
    page.set_default_timeout(60000)  # 60 секунд
    return page

# Или используйте явные ожидания
def test_slow_page(page):
    page.goto("https://slow-website.com")
    page.wait_for_selector("#loaded-content", timeout=30000)
```

## 🐳 Проблемы с Docker

#### **Ошибка: "docker: command not found"**
**Решение:**
1. Установите Docker Desktop (Windows/Mac) или Docker Engine (Linux)
2. Добавьте Docker в PATH
3. Перезапустите терминал

#### **Ошибка при сборке образа**
**Решение:**
```dockerfile
# Проверьте Dockerfile на ошибки
# Убедитесь, что все файлы находятся в контексте сборки
# Используйте .dockerignore для исключения ненужных файлов

# Сборка с подробным выводом
docker build --no-cache -t my-test-image .
```

#### **Контейнер не запускается**
**Решение:**
```bash
# Проверьте логи
docker logs container_name

# Запустите с интерактивным режимом
docker run -it --entrypoint bash my-test-image

# Проверьте порты и сети
docker inspect container_name
```

## 🔧 Git и GitHub проблемы

#### **Ошибка: "fatal: not a git repository"**
**Решение:**
```bash
# Инициализируйте репозиторий
git init
git remote add origin https://github.com/username/repo.git

# Или клонируйте существующий
git clone https://github.com/username/repo.git
```

#### **Ошибка авторизации при push**
**Решение:**
```bash
# Используйте Personal Access Token вместо пароля
git remote set-url origin https://username:token@github.com/username/repo.git

# Или настройте SSH ключи
ssh-keygen -t ed25519 -C "your_email@example.com"
# Добавьте ключ в GitHub Settings -> SSH and GPG keys
```

## 💡 Полезные команды диагностики

### Python и окружение
```bash
python --version
pip --version
pip list
which python  # Linux/Mac
where python  # Windows
echo $PATH    # Linux/Mac
echo %PATH%   # Windows
```

### Git
```bash
git status
git log --oneline -10
git remote -v
git config --list
```

### Docker
```bash
docker --version
docker info
docker images
docker ps -a
docker system df
```

### Системная информация
```bash
# Windows
systeminfo
# Linux
uname -a
cat /etc/os-release
# Mac
sw_vers
```

## 🆘 Когда обращаться за помощью

### Соберите информацию перед обращением:
- [ ] Версия Python (`python --version`)
- [ ] Версия pip (`pip --version`)
- [ ] Операционная система и версия
- [ ] Точный текст ошибки
- [ ] Команды, которые привели к ошибке
- [ ] Что вы уже пробовали

### Где искать помощь:
- **Stack Overflow** - для технических вопросов
- **GitHub Issues** - для багов в инструментах
- **Discord/Slack сообщества** - для оперативной помощи
- **Официальная документация** - первоисточник информации

## 📝 Шаблон для сообщения о проблеме

```
**Проблема:** [Краткое описание проблемы]

**Окружение:**
- ОС: [например, Windows 11, Ubuntu 20.04]
- Python версия: [например, 3.11.0]
- Версии пакетов: [pip list]
- Docker версия (если используется): [docker --version]

**Шаги для воспроизведения:**
1. [Первый шаг]
2. [Второй шаг]
3. [и т.д.]

**Ожидаемое поведение:**
[Что должно было произойти]

**Фактическое поведение:**
[Что произошло на самом деле]

**Логи/ошибки:**
```
[Вставьте полный текст ошибки]
```

**Что я уже пробовал:**
- [Попытка 1]
- [Попытка 2]
```