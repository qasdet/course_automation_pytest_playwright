"""
Пример 2: Типы данных и операции
Тема: Работа с числами, строками и логическими значениями
"""

# === ЧИСЛОВЫЕ ТИПЫ ===
print("=== ЧИСЛОВЫЕ ТИПЫ ===")

# Целые числа
age = 25
quantity = 100

# Вещественные числа
price = 999.99
discount_rate = 0.15  # 15%

# Арифметические операции
original_price = 1299.99
discount_amount = original_price * discount_rate
final_price = original_price - discount_amount

print(f"Цена товара: {original_price} руб.")
print(f"Скидка: {discount_rate * 100}% ({discount_amount:.2f} руб.)")
print(f"Итоговая цена: {final_price:.2f} руб.")
print()

# === СТРОКОВЫЕ ТИПЫ ===
print("=== СТРОКОВЫЕ ТИПЫ ===")

# Создание строк
first_name = "Иван"
last_name = "Петров"
email = "ivan.petrov@example.com"

# Конкатенация строк
full_name = first_name + " " + last_name
welcome_message = "Здравствуйте, " + full_name + "!"

print(welcome_message)
print(f"Email: {email}")
print()

# f-строки (форматированные строки)
order_number = 12345
order_date = "15.01.2024"
order_total = 2599.98

order_info = f"""
=== ИНФОРМАЦИЯ О ЗАКАЗЕ ===
Номер заказа: {order_number}
Дата заказа: {order_date}
Сумма заказа: {order_total:.2f} руб.
Статус: {'Обработан' if order_total > 0 else 'Ошибка'}
============================
"""

print(order_info)

# Методы строк
product_name = "  Ноутбук Apple MacBook Pro  "
print(f"Оригинал: '{product_name}'")
print(f"Без пробелов: '{product_name.strip()}'")
print(f"В верхнем регистре: '{product_name.upper()}'")
print(f"В нижнем регистре: '{product_name.lower()}'")
print(f"Длина строки: {len(product_name)} символов")
print()

# === ЛОГИЧЕСКИЙ ТИП ===
print("=== ЛОГИЧЕСКИЙ ТИП ===")

# Логические значения
is_authenticated = True
has_permission = False
is_admin = True

# Логические операции
can_access_system = is_authenticated and has_permission
can_edit_content = is_authenticated and (has_permission or is_admin)
show_admin_panel = is_authenticated and is_admin

print(f"Авторизован: {is_authenticated}")
print(f"Есть права доступа: {has_permission}")
print(f"Администратор: {is_admin}")
print()
print(f"Может войти в систему: {can_access_system}")
print(f"Может редактировать: {can_edit_content}")
print(f"Показать админ-панель: {show_admin_panel}")
print()

# === ПРАКТИЧЕСКИЙ ПРИМЕР ===
print("=== КАЛЬКУЛЯТОР СКИДОК ===")

def calculate_discount(total_amount):
    """Рассчитывает скидку в зависимости от суммы заказа"""
    if total_amount >= 5000:
        discount = 0.15  # 15%
        discount_name = "Премиум"
    elif total_amount >= 3000:
        discount = 0.10  # 10%
        discount_name = "Золотой"
    elif total_amount >= 1000:
        discount = 0.05  # 5%
        discount_name = "Серебряный"
    else:
        discount = 0     # 0%
        discount_name = "Без скидки"
    
    discount_amount = total_amount * discount
    final_amount = total_amount - discount_amount
    
    return {
        'original': total_amount,
        'discount_percent': discount * 100,
        'discount_name': discount_name,
        'discount_amount': discount_amount,
        'final_amount': final_amount
    }

# Тестирование функции
test_amounts = [800, 1500, 3500, 6000]

for amount in test_amounts:
    result = calculate_discount(amount)
    print(f"Сумма заказа: {amount} руб.")
    print(f"Тип скидки: {result['discount_name']}")
    print(f"Скидка: {result['discount_percent']}% ({result['discount_amount']:.2f} руб.)")
    print(f"К оплате: {result['final_amount']:.2f} руб.")
    print("-" * 40)