#!/bin/bash

# setup_environment.sh - Bash скрипт настройки окружения для Linux/Mac

set -e  # Останавливать выполнение при ошибках

echo "🚀 Автоматическая настройка окружения"
echo "Курс: Автоматизация тестирования с Python, pytest и Playwright"
echo

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Проверка версии Python
check_python() {
    print_status "Проверка Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
        if [[ "$PYTHON_VERSION" < "3.10" ]]; then
            print_error "Требуется Python 3.10+, найден $PYTHON_VERSION"
            return 1
        fi
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        print_error "Python не найден"
        return 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version)
    print_success "Найден $PYTHON_VERSION"
}

# Установка системных зависимостей (Ubuntu/Debian)
install_system_deps() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_status "Проверка системных зависимостей..."
        
        # Проверка, является ли пользователь root
        if [[ $EUID -eq 0 ]]; then
            print_warning "Запущено от root. Продолжить? (y/N)"
            read -r response
            if [[ ! "$response" =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
        
        # Обновление пакетов
        if command -v apt &> /dev/null; then
            print_status "Обновление системных пакетов..."
            sudo apt update
            
            print_status "Установка системных зависимостей..."
            sudo apt install -y \
                python3-venv \
                python3-dev \
                build-essential \
                libssl-dev \
                libffi-dev \
                curl \
                wget
        fi
    fi
}

# Настройка виртуального окружения
setup_venv() {
    print_status "Настройка виртуального окружения..."
    
    # Удаление старого окружения
    if [ -d ".venv" ]; then
        print_warning "Удаление существующего виртуального окружения..."
        rm -rf .venv
    fi
    
    # Создание нового окружения
    $PYTHON_CMD -m venv .venv
    print_success "Виртуальное окружение создано"
    
    # Активация
    source .venv/bin/activate
    print_success "Виртуальное окружение активировано"
}

# Обновление pip
upgrade_pip() {
    print_status "Обновление pip..."
    python -m pip install --upgrade pip
    print_success "pip обновлен"
}

# Установка зависимостей
install_requirements() {
    if [ -f "requirements.txt" ]; then
        print_status "Установка зависимостей..."
        pip install -r requirements.txt
        print_success "Зависимости установлены"
    else
        print_warning "Файл requirements.txt не найден"
    fi
}

# Установка Playwright
install_playwright() {
    print_status "Установка Playwright..."
    pip install playwright
    print_success "Playwright установлен"
    
    print_status "Установка браузеров Playwright..."
    playwright install --with-deps
    print_success "Браузеры Playwright установлены"
}

# Тестирование установки
test_installation() {
    print_status "Тестирование установки..."
    
    # Тест Python
    python --version > /dev/null && print_success "Python работает"
    
    # Тест pytest
    if python -c "import pytest" 2>/dev/null; then
        print_success "pytest доступен"
    else
        print_warning "pytest не найден"
    fi
    
    # Тест Playwright
    if python -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
        print_success "Playwright доступен"
    else
        print_warning "Playwright не найден"
    fi
    
    # Тест браузера
    if python << 'EOF' 2>/dev/null; then
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    title = page.title()
    browser.close()
print("Browser test: OK")
EOF
        print_success "Браузер работает корректно"
    else
        print_warning "Проблемы с запуском браузера"
    fi
}

# Создание отчета
create_report() {
    print_status "Создание отчета..."
    
    cat > setup_report.md << EOF
# Отчет о настройке окружения

## Системная информация
- ОС: $(uname -s) $(uname -r)
- Архитектура: $(uname -m)
- Дата: $(date)

## Результаты
✅ Настройка завершена успешно!

## Следующие шаги
1. Активируйте виртуальное окружение: \`source .venv/bin/activate\`
2. Запустите тесты: \`pytest\`
3. Перейдите к следующему этапу курса
EOF

    print_success "Отчет сохранен в setup_report.md"
}

# Основной процесс
main() {
    echo "Начало настройки..."
    echo
    
    # Проверка Python
    if ! check_python; then
        exit 1
    fi
    
    # Установка системных зависимостей
    install_system_deps
    
    # Настройка виртуального окружения
    setup_venv
    
    # Обновление и установка
    upgrade_pip
    install_requirements
    install_playwright
    
    # Тестирование
    test_installation
    
    # Создание отчета
    create_report
    
    echo
    print_success "🎉 Настройка завершена!"
    echo
    echo "Для активации окружения выполните:"
    echo "source .venv/bin/activate"
    echo
    echo "Для проверки установки:"
    echo "python -c \"import pytest; print('OK')\""
    echo
}

# Запуск основного процесса
main "$@"