# setup_environment.ps1 - PowerShell скрипт настройки окружения для Windows

param(
    [switch]$Force = $false,
    [switch]$SkipTests = $false
)

# Цвета для вывода
$host.UI.RawUI.ForegroundColor = "White"

function Write-Status {
    param([string]$Message)
    Write-Host "🔧 $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
}

# Проверка прав администратора
function Test-AdminRights {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Проверка версии Python
function Test-PythonVersion {
    Write-Status "Проверка Python..."
    
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            $pythonVersion = python3 --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                $script:PythonCmd = "python3"
                $script:PipCmd = "pip3"
            } else {
                throw "Python не найден"
            }
        } else {
            $script:PythonCmd = "python"
            $script:PipCmd = "pip"
        }
        
        $versionString = $pythonVersion -split " ")[1]
        $majorVersion = [int]($versionString -split "\.")[0]
        $minorVersion = [int]($versionString -split "\.")[1]
        
        if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 10)) {
            throw "Требуется Python 3.10+, найден $versionString"
        }
        
        Write-Success "Найден Python $versionString"
        return $true
    }
    catch {
        Write-Error $_.Exception.Message
        return $false
    }
}

# Настройка виртуального окружения
function Setup-VirtualEnvironment {
    Write-Status "Настройка виртуального окружения..."
    
    # Удаление старого окружения если указан флаг Force
    if (Test-Path ".venv") {
        if ($Force) {
            Write-Warning "Удаление существующего виртуального окружения..."
            Remove-Item ".venv" -Recurse -Force
        } else {
            Write-Warning "Виртуальное окружение уже существует. Используйте -Force для пересоздания."
        }
    }
    
    # Создание нового окружения
    try {
        & $script:PythonCmd -m venv .venv
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Виртуальное окружение создано"
            return $true
        } else {
            throw "Ошибка создания виртуального окружения"
        }
    }
    catch {
        Write-Error $_.Exception.Message
        return $false
    }
}

# Активация виртуального окружения
function Activate-VirtualEnvironment {
    Write-Status "Активация виртуального окружения..."
    
    try {
        $activateScript = ".\.venv\Scripts\Activate.ps1"
        if (Test-Path $activateScript) {
            & $activateScript
            Write-Success "Виртуальное окружение активировано"
            return $true
        } else {
            throw "Скрипт активации не найден"
        }
    }
    catch {
        Write-Error $_.Exception.Message
        return $false
    }
}

# Обновление pip
function Update-Pip {
    Write-Status "Обновление pip..."
    
    try {
        & $script:PythonCmd -m pip install --upgrade pip
        if ($LASTEXITCODE -eq 0) {
            Write-Success "pip обновлен"
            return $true
        } else {
            throw "Ошибка обновления pip"
        }
    }
    catch {
        Write-Error $_.Exception.Message
        return $false
    }
}

# Установка зависимостей
function Install-Dependencies {
    Write-Status "Установка зависимостей..."
    
    if (Test-Path "requirements.txt") {
        try {
            pip install -r requirements.txt
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Зависимости установлены"
                return $true
            } else {
                throw "Ошибка установки зависимостей"
            }
        }
        catch {
            Write-Error $_.Exception.Message
            return $false
        }
    } else {
        Write-Warning "Файл requirements.txt не найден"
        return $false
    }
}

# Установка Playwright
function Install-Playwright {
    Write-Status "Установка Playwright..."
    
    try {
        pip install playwright
        if ($LASTEXITCODE -ne 0) {
            throw "Ошибка установки Playwright"
        }
        
        Write-Status "Установка браузеров Playwright..."
        playwright install
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Playwright и браузеры установлены"
            return $true
        } else {
            throw "Ошибка установки браузеров"
        }
    }
    catch {
        Write-Error $_.Exception.Message
        return $false
    }
}

# Тестирование установки
function Test-Installation {
    if ($SkipTests) {
        Write-Warning "Пропущено тестирование установки"
        return $true
    }
    
    Write-Status "Тестирование установки..."
    
    $testResults = @()
    
    # Тест Python
    try {
        & $script:PythonCmd --version > $null
        Write-Success "Python работает"
        $testResults += $true
    }
    catch {
        Write-Error "Python не работает"
        $testResults += $false
    }
    
    # Тест pytest
    try {
        & $script:PythonCmd -c "import pytest" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "pytest доступен"
            $testResults += $true
        } else {
            Write-Warning "pytest не найден"
            $testResults += $false
        }
    }
    catch {
        Write-Warning "pytest не найден"
        $testResults += $false
    }
    
    # Тест Playwright
    try {
        & $script:PythonCmd -c "from playwright.sync_api import sync_playwright" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Playwright доступен"
            $testResults += $true
        } else {
            Write-Warning "Playwright не найден"
            $testResults += $false
        }
    }
    catch {
        Write-Warning "Playwright не найден"
        $testResults += $false
    }
    
    # Подсчет успешных тестов
    $successCount = ($testResults | Where-Object { $_ -eq $true } | Measure-Object).Count
    $totalCount = $testResults.Count
    
    if ($successCount -eq $totalCount) {
        Write-Success "Все тесты пройдены ($successCount/$totalCount)"
        return $true
    } else {
        Write-Warning "Пройдено тестов: $successCount/$totalCount"
        return $false
    }
}

# Создание отчета
function Create-Report {
    Write-Status "Создание отчета..."
    
    $reportContent = @"
# Отчет о настройке окружения

## Системная информация
- ОС: $((Get-CimInstance Win32_OperatingSystem).Caption)
- Версия: $((Get-CimInstance Win32_OperatingSystem).Version)
- Архитектура: $((Get-CimInstance Win32_Processor).Architecture)
- Дата: $(Get-Date)

## Результаты
✅ Настройка завершена успешно!

## Следующие шаги
1. Активируйте виртуальное окружение: `.\.venv\Scripts\Activate.ps1`
2. Запустите тесты: `pytest`
3. Перейдите к следующему этапу курса
"@
    
    $reportContent | Out-File -FilePath "setup_report.md" -Encoding UTF8
    Write-Success "Отчет сохранен в setup_report.md"
}

# Основной процесс
function Main {
    Write-Header "Автоматическая настройка окружения"
    Write-Host "Курс: Автоматизация тестирования с Python, pytest и Playwright"
    Write-Host ""
    
    # Проверка прав администратора
    if (Test-AdminRights) {
        Write-Warning "Скрипт запущен с правами администратора. Это может быть небезопасно."
        if (-not $Force) {
            $response = Read-Host "Продолжить? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                exit 1
            }
        }
    }
    
    $steps = @(
        @{Name = "Проверка Python"; Action = { Test-PythonVersion }},
        @{Name = "Настройка виртуального окружения"; Action = { Setup-VirtualEnvironment }},
        @{Name = "Активация виртуального окружения"; Action = { Activate-VirtualEnvironment }},
        @{Name = "Обновление pip"; Action = { Update-Pip }},
        @{Name = "Установка зависимостей"; Action = { Install-Dependencies }},
        @{Name = "Установка Playwright"; Action = { Install-Playwright }},
        @{Name = "Тестирование установки"; Action = { Test-Installation }},
        @{Name = "Создание отчета"; Action = { Create-Report }}
    )
    
    $successfulSteps = 0
    
    foreach ($step in $steps) {
        Write-Header $step.Name
        
        try {
            if (& $step.Action) {
                $successfulSteps++
            } else {
                Write-Error "Шаг '$($step.Name)' завершился с ошибкой"
            }
        }
        catch {
            Write-Error "Ошибка в шаге '$($step.Name)': $($_.Exception.Message)"
        }
    }
    
    # Финальный отчет
    Write-Header "Результаты настройки"
    Write-Host "✅ Успешно выполнено шагов: $successfulSteps/$($steps.Count)"
    
    if ($successfulSteps -eq $steps.Count) {
        Write-Host ""
        Write-Success "🎉 Настройка завершена успешно!"
        Write-Host ""
        Write-Host "Для продолжения:"
        Write-Host "1. Активируйте виртуальное окружение:"
        Write-Host "   .\.venv\Scripts\Activate.ps1"
        Write-Host "2. Перейдите к следующему этапу курса"
    } else {
        Write-Host ""
        Write-Warning "Настройка завершена с ошибками"
        Write-Host "Проверьте вывод выше и исправьте проблемы"
    }
}

# Запуск основного процесса
Main