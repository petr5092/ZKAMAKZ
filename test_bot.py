# test_bot.py
import sys
import os

print("🔍 ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
print("=" * 50)

# Текущая директория
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Текущая папка: {current_dir}")

# Проверяем существование файлов и папок
items_to_check = [
    'app/main.py',
    'app/config.py', 
    'app/database.py',
    'requirements.txt',
    'docker-compose.yml'
]

print("\n📁 ПРОВЕРКА ФАЙЛОВ:")
for item in items_to_check:
    full_path = os.path.join(current_dir, item)
    if os.path.exists(full_path):
        print(f"✅ {item} - найден")
    else:
        print(f"❌ {item} - не найден")

# Проверяем импорты из папки app
print("\n🔧 ПРОВЕРКА ИМПОРТОВ ИЗ APP:")
try:
    # Добавляем папку app в путь Python
    app_path = os.path.join(current_dir, 'app')
    if os.path.exists(app_path):
        sys.path.insert(0, app_path)
        print("✅ Папка app добавлена в путь Python")
        
        # Пробуем импортировать основные модули
        try:
            from main import UniversityDataProvider, UniversityStyler, ButtonFactory
            print("✅ main.py - импортирован успешно")
            
            # Тестируем компоненты
            print("\n🧪 ТЕСТИРОВАНИЕ КОМПОНЕНТОВ:")
            universities = UniversityDataProvider.get_all_universities()
            print(f"✅ Университеты: {len([u for u in universities if u])} шт")
            
            if universities and universities[0]:
                formatted = UniversityStyler.format_university_info(universities[0])
                print("✅ Стилизация: РАБОТАЕТ")
                print("\n📋 Пример университета:")
                print("=" * 40)
                print(formatted)
                print("=" * 40)
            
            buttons = ButtonFactory.create_main_menu_buttons()
            print(f"✅ Кнопки: {len(buttons)} ряда создано")
            
        except ImportError as e:
            print(f"❌ Ошибка импорта из main.py: {e}")
            
    else:
        print("❌ Папка app не найдена")
        
except Exception as e:
    print(f"❌ Общая ошибка: {e}")

print("\n🎯 СЛЕДУЮЩИЕ ШАГИ:")
print("1. Запустите бота: python app/main.py")
print("2. Или из папки app: cd app && python main.py")