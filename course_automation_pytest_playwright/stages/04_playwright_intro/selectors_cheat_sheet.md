# 🎯 Шаблоны локаторов и селекторов Playwright

## 📋 Общие принципы выбора селекторов

### Приоритет селекторов (от лучшего к худшему):
1. **Тестовые атрибуты** - `data-testid`, `data-test`, `data-cy`
2. **ID элементов** - `#unique-id`
3. **Текстовые селекторы** - `text="Exact text"` или `text="Partial text"`
4. **CSS классы** - `.class-name`
5. **Структурные селекторы** - `div > span`
6. **XPath** - только когда другие варианты невозможны

## 🔧 Шаблоны селекторов по типам элементов

### Формы и поля ввода

```python
# Поля ввода
page.locator("input[name='username']")
page.locator("input#email")
page.locator("input[type='email']")
page.locator("input[data-testid='email-input']")

# Текстовые поля
page.locator("textarea[name='message']")
page.locator("textarea#description")

# Password поля
page.locator("input[type='password']")
page.locator("#password-field")

# Числовые поля
page.locator("input[type='number']")
page.locator("input[min][max]")

# Поля поиска
page.locator("input[type='search']")
page.locator("input[placeholder*='search' i]")
```

### Кнопки и ссылки

```python
# Кнопки
page.locator("button[type='submit']")
page.locator("button.primary")
page.locator("button[data-action='save']")
page.locator("text='Save Changes'")
page.locator("button:has-text('Submit')")

# Ссылки
page.locator("a[href='/dashboard']")
page.locator("a:has-text('Learn More')")
page.locator("link[rel='canonical']")
page.locator("a[target='_blank']")
```

### Выпадающие списки и селекты

```python
# Стандартные select
page.locator("select[name='country']")
page.locator("select#category")
page.locator("select[data-role='dropdown']")

# Custom dropdowns
page.locator(".dropdown-toggle")
page.locator("[role='combobox']")
page.locator(".select-wrapper")

# Options
page.locator("option[value='us']")
page.locator("option:has-text('United States')")
```

### Чекбоксы и радио кнопки

```python
# Чекбоксы
page.locator("input[type='checkbox']")
page.locator("input[name='agreement']")
page.locator("#accept-terms")

# Радио кнопки
page.locator("input[type='radio']")
page.locator("input[name='gender'][value='male']")
page.locator(".radio-option input")
```

### Навигация и меню

```python
# Навигационные элементы
page.locator("nav a")
page.locator(".navbar-brand")
page.locator("ul.nav li a")

# Меню
page.locator(".menu-item")
page.locator("[role='menuitem']")
page.locator(".dropdown-menu a")

# Хлебные крошки
page.locator(".breadcrumb a")
page.locator("nav[aria-label='breadcrumb'] a")
```

### Таблицы

```python
# Таблицы
page.locator("table.data-table")
page.locator(".table-responsive table")

# Ячейки таблицы
page.locator("td:first-child")
page.locator("tr:nth-child(2) td:last-child")
page.locator("table tbody tr td[data-column='name']")

# Заголовки таблицы
page.locator("th.sortable")
page.locator("table thead th")
```

### Модальные окна и попапы

```python
# Модальные окна
page.locator(".modal.show")
page.locator("[role='dialog']")
page.locator(".popup-overlay")

# Кнопки закрытия
page.locator(".modal-close")
page.locator("[data-dismiss='modal']")
page.locator(".close-button")
```

## 🎯 Продвинутые шаблоны селекторов

### Chain селекторы

```python
# Поиск внутри элемента
form = page.locator("form.login")
username = form.locator("input#username")
password = form.locator("input#password")
submit_btn = form.locator("button[type='submit']")

# Множественные условия
page.locator("button").filter(has_text="Submit").filter(visible=True)
page.locator("input").filter(enabled=True).filter(empty=True)

# Поиск по позиции
page.locator("li").nth(0)  # Первый элемент
page.locator("tr").first    # Первый ряд
page.locator("td").last     # Последняя ячейка
```

### Фильтры и псевдоселекторы

```python
# Состояния элементов
page.locator("button").filter(visible=True)
page.locator("input").filter(enabled=True)
page.locator("option").filter(selected=True)
page.locator("a").filter(attached=True)

# Содержание текста
page.locator("div").filter(has_text="Important")
page.locator("span").filter(has_text=re.compile(r"^\d+$"))

# Поиск по дочерним элементам
page.locator("form").filter(has=page.locator("input[type='submit']"))
```

### Регулярные выражения

```python
import re

# Текст по регулярному выражению
page.locator(re.compile(r"Price: \$\d+"))

# Атрибуты по регулярному выражению
page.locator("[href*=dashboard]")
page.locator("[class*=button]")
```

## 📱 Mobile-специфичные селекторы

```python
# Мобильные меню
page.locator(".mobile-menu-toggle")
page.locator(".hamburger-menu")
page.locator("[data-mobile='menu-toggle']")

# Touch элементы
page.locator(".touch-target")
page.locator("[touch-action]")
page.locator(".swipe-area")

# Адаптивные элементы
page.locator(".desktop-hidden")
page.locator(".mobile-only")
```

## 🔄 Динамические селекторы

```python
# Элементы с динамическими ID
page.locator("[id^='user_']")  # Начинается с 'user_'
page.locator("[id$='_button']")  # Заканчивается на '_button'
page.locator("[id*='dynamic']")  # Содержит 'dynamic'

# Элементы с динамическими классами
page.locator("[class~='active']")  # Содержит класс 'active'
page.locator("[class|='btn']")  # Начинается с 'btn'

# По data-атрибутам
page.locator("[data-status='pending']")
page.locator("[data-type='notification']")
```

## 🎨 Специфичные для сайтов шаблоны

### Bootstrap сайты
```python
# Bootstrap кнопки
page.locator(".btn.btn-primary")
page.locator(".btn:has-text('Submit')")

# Bootstrap формы
page.locator(".form-control")
page.locator(".form-group input")

# Bootstrap модальные окна
page.locator(".modal.fade.show")
page.locator(".modal-dialog")
```

### Material Design сайты
```python
# Material кнопки
page.locator(".mat-button")
page.locator(".mat-raised-button")

# Material input поля
page.locator(".mat-input-element")
page.locator("mat-form-field input")

# Material селекты
page.locator("mat-select")
page.locator(".mat-select-panel")
```

## ⚡ Оптимизированные шаблоны

### Для стабильности
```python
# Предпочтительные стабильные селекторы
page.locator("[data-testid='submit-button']")  # Тестовые атрибуты
page.locator("#unique-form-id button")         # ID + тег
page.locator("text='Exact Button Text'")       # Точный текст

# Избегать нестабильные селекторы
# ❌ page.locator("div:nth-child(3) span")
# ❌ page.locator(".container > div > button")
# ❌ page.locator("[class*='button']")
```

### Для производительности
```python
# Быстрые селекторы
page.locator("#id")              # Самый быстрый
page.locator("[data-testid]")    # Очень быстрый
page.locator("tag.class")        # Быстрый

# Медленные селекторы (использовать осторожно)
# page.locator("*:has-text('text')")  # Очень медленный
# page.locator("xpath=//div//span")   # Медленный
```

## 🛠️ Утилитные функции для селекторов

```python
class SelectorBuilder:
    """Помощник для построения селекторов"""
    
    @staticmethod
    def by_test_id(test_id: str) -> str:
        """Селектор по тестовому ID"""
        return f"[data-testid='{test_id}']"
    
    @staticmethod
    def by_role(role: str, name: str = None) -> str:
        """Селектор по роли ARIA"""
        if name:
            return f"[role='{role}'][aria-label='{name}']"
        return f"[role='{role}']"
    
    @staticmethod
    def clickable_button(text: str) -> str:
        """Селектор кликабельной кнопки"""
        return f"button:has-text('{text}'):not([disabled])"
    
    @staticmethod
    def required_field(name: str) -> str:
        """Селектор обязательного поля"""
        return f"input[name='{name}'][required]"
    
    @staticmethod
    def error_message(field_name: str) -> str:
        """Селектор сообщения об ошибке"""
        return f"[data-error-for='{field_name}']"

# Использование:
# locator = page.locator(SelectorBuilder.by_test_id("username"))
# submit_btn = page.locator(SelectorBuilder.clickable_button("Submit"))
```

## 📊 Матрица выбора селекторов

| Тип элемента | Лучший селектор | Альтернативы | Избегать |
|-------------|----------------|--------------|----------|
| Кнопка Submit | `[data-testid='submit']` | `button[type='submit']` | `div:nth-child(2) button` |
| Поле Email | `input[type='email']` | `#email` | `.form-group:nth-child(1) input` |
| Навигационная ссылка | `a[href='/dashboard']` | `nav a:has-text('Dashboard')` | `div > ul > li > a` |
| Модальное окно | `[role='dialog']` | `.modal.show` | `.popup-container div` |
| Таблица данных | `table.data-table` | `#results-table` | `div.table-wrapper table` |

## 🎯 Best Practices

1. **Используйте тестовые атрибуты** когда возможно
2. **Будьте_specific** - избегайте слишком общих селекторов
3. **Учитывайте контекст** - используйте chain локаторы
4. **Тестируйте селекторы** отдельно перед использованием
5. **Документируйте сложные селекторы** с комментариями
6. **Регулярно рефакторите** селекторы для улучшения стабильности