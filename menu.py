import os
import subprocess
from colorama import init, Fore

# Инициализация colorama для поддержки цветов в консоли
init()

def show_menu():
    print(Fore.CYAN + "--- МЕНЮ ---")
    print("1. Показать все элементы")
    print("2. Запустить скрипт")
    print("3. Выход")

def show_all_items():
    print(Fore.YELLOW + "--- Все элементы ---")
    # Здесь можно добавить логику для вывода всех элементов

def run_script(script_path):
    print(Fore.GREEN + f"--- Запуск скрипта {script_path} ---")
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Ошибка при выполнении скрипта: {e}")
    except Exception as e:
        print(Fore.RED + f"Ошибка: {e}")

# Словарь с путями к скриптам
script_paths = {
    "1": "o1d-collector/1-read_collection.py",
    "2": "o1d-collector/downloader.py",
    "3": "o1d-collector/exporter.py",
    "4": "o1d-collector/jsonmerger.py",
    "5": "o1d-collector/duplicate_cleaner.py"
}

# Словарь с именами скриптов
script_names = {
    "1": "Конвертация коллекции",
    "2": "Загрузчик карт по коллекции",
    "3": "Экспорт коллекций",
    "4": "Объединение json файлов",
    "5": "Очистка дубликатов карт"
}

# Получение текущей директории
current_directory = os.path.dirname(os.path.abspath(__file__))

# Преобразование путей скриптов в относительные пути
for key in script_paths:
    script_paths[key] = os.path.join(current_directory, script_paths[key])

# Главный цикл программы
while True:
    show_menu()
    choice = input(Fore.MAGENTA + "Выберите пункт меню: ")
    
    if choice == "1":
        show_all_items()
    elif choice == "2":
        print(Fore.YELLOW + "--- Доступные скрипты ---")
        for key in script_paths:
            print(f"{Fore.GREEN}{key}. {script_names[key]}")
        script_choice = input(Fore.MAGENTA + "Выберите скрипт: ")
        if script_choice in script_paths:
            script_path = script_paths[script_choice]
            if os.path.exists(script_path):
                run_script(script_path)
            else:
                print(Fore.RED + "Указанный скрипт не найден.")
        else:
            print(Fore.RED + "Некорректный выбор скрипта.")
    elif choice == "3":
        print(Fore.YELLOW + "Выход из программы...")
        break
    else:
        print(Fore.RED + "Некорректный выбор. Пожалуйста, попробуйте снова.")
