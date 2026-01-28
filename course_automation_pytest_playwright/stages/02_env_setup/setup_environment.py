#!/usr/bin/env python3
"""
setup_environment.py - Скрипт автоматической настройки окружения

Этот скрипт автоматизирует процесс настройки рабочего окружения
для курса по автоматизации тестирования с Python, pytest и Playwright.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def print_section(title):
    """Печать разделителя с заголовком"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def run_command(command, description="", cwd=None):
    """Выполнение команды с обработкой ошибок"""
    print(f"\n🔧 {description}")
    print(f"Команда: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        
        if result.returncode == 0:
            print("✅ Успешно")
            if result.stdout.strip():
                print(f"Вывод: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ошибка")
            print(f"stderr: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False


def check_python_version():
    """Проверка версии Python"""
    print_section("Проверка Python")
    
    version = sys.version_info
    print(f"Найден Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("✅ Версия Python подходит")
        return True
    else:
        print("❌ Требуется Python 3.10 или выше")
        return False


def setup_virtual_environment():
    """Настройка виртуального окружения"""
    print_section("Настройка виртуального окружения")
    
    venv_path = Path(".venv")
    
    # Удаление существующего окружения
    if venv_path.exists():
        print("⚠️  Удаление существующего виртуального окружения...")
        shutil.rmtree(venv_path)
    
    # Создание нового окружения
    if run_command("python -m venv .venv", "Создание виртуального окружения"):
        print("✅ Виртуальное окружение создано")
        
        # Активация (для текущей сессии)
        if platform.system() == "Windows":
            activate_script = ".venv\\Scripts\\activate.bat"
        else:
            activate_script = "source .venv/bin/activate"
            
        print(f"Для активации используйте: {activate_script}")
        return True
    
    return False


def upgrade_pip():
    """Обновление pip"""
    print_section("Обновление pip")
    
    return run_command(
        "python -m pip install --upgrade pip",
        "Обновление pip до последней версии"
    )


def install_dependencies():
    """Установка зависимостей"""
    print_section("Установка зависимостей")
    
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ Файл requirements.txt не найден")
        return False
    
    return run_command(
        "pip install -r requirements.txt",
        "Установка зависимостей из requirements.txt"
    )


def install_playwright_browsers():
    """Установка браузеров Playwright"""
    print_section("Установка браузеров Playwright")
    
    # Установка Playwright если еще не установлен
    run_command("pip install playwright", "Установка Playwright")
    
    # Установка браузеров
    install_cmd = "playwright install"
    
    # На Linux добавляем --with-deps
    if platform.system() != "Windows":
        install_cmd += " --with-deps"
    
    return run_command(install_cmd, "Установка браузеров Playwright")


def test_setup():
    """Тестирование настройки"""
    print_section("Тестирование настройки")
    
    test_code = '''
import sys
print(f"Python: {sys.version}")

try:
    import pytest
    print(f"pytest: {pytest.__version__}")
except ImportError:
    print("pytest: не установлен")

try:
    import playwright
    print(f"playwright: {playwright.__version__}")
except ImportError:
    print("playwright: не установлен")

try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        title = page.title()
        print(f"Browser test: {title}")
        browser.close()
        print("Browser test: ✅ Успешно")
except Exception as e:
    print(f"Browser test: ❌ Ошибка - {e}")
'''
    
    return run_command(
        f'python -c "{test_code}"',
        "Тестирование установленных пакетов"
    )


def create_setup_report():
    """Создание отчета о настройке"""
    print_section("Создание отчета")
    
    report_content = f"""# Отчет о настройке окружения

## Системная информация
- Операционная система: {platform.system()} {platform.release()}
- Архитектура: {platform.machine()}
- Python: {sys.version}

## Время настройки
{platform.node()} - {platform.platform()}

## Результаты проверок
- Python версия: {'✅' if check_python_version() else '❌'}
- Виртуальное окружение: {'✅' if Path('.venv').exists() else '❌'}
- Зависимости: {'✅' if Path('requirements.txt').exists() else '❌'}

## Следующие шаги
1. Активируйте виртуальное окружение
2. Запустите тесты: `pytest`
3. Проверьте работу Playwright: `playwright codegen`
"""

    with open("setup_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print("✅ Отчет сохранен в setup_report.md")
    return True


def main():
    """Основная функция настройки"""
    print("🚀 Автоматическая настройка окружения")
    print("Курс: Автоматизация тестирования с Python, pytest и Playwright")
    
    # Проверка прав доступа
    if os.geteuid() == 0:
        print("⚠️  Рекомендуется запускать без прав root/sudo")
    
    steps = [
        ("Проверка Python", check_python_version),
        ("Настройка виртуального окружения", setup_virtual_environment),
        ("Обновление pip", upgrade_pip),
        ("Установка зависимостей", install_dependencies),
        ("Установка браузеров Playwright", install_playwright_browsers),
        ("Тестирование настройки", test_setup),
        ("Создание отчета", create_setup_report)
    ]
    
    successful_steps = 0
    
    for step_name, step_func in steps:
        try:
            if step_func():
                successful_steps += 1
            else:
                print(f"❌ Шаг '{step_name}' завершился с ошибкой")
        except Exception as e:
            print(f"❌ Ошибка в шаге '{step_name}': {e}")
    
    # Финальный отчет
    print_section("Результаты настройки")
    print(f"✅ Успешно выполнено шагов: {successful_steps}/{len(steps)}")
    
    if successful_steps == len(steps):
        print("🎉 Настройка завершена успешно!")
        print("\nДля продолжения:")
        print("1. Активируйте виртуальное окружение:")
        if platform.system() == "Windows":
            print("   .\\.venv\\Scripts\\Activate.ps1")
        else:
            print("   source .venv/bin/activate")
        print("2. Перейдите к следующему этапу курса")
    else:
        print("⚠️  Настройка завершена с ошибками")
        print("Проверьте вывод выше и исправьте проблемы")
    
    return successful_steps == len(steps)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)