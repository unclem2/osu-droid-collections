import os
import pickle
from colorama import init, Fore, Style

init() # инициализация colorama

# Определяем текущую директорию
current_dir = os.path.dirname(os.path.abspath(__file__))

# Проверяем, есть ли файл со списком скриптов, и если есть, загружаем его
scripts_file_path = os.path.join(current_dir, 'scripts.pickle')
if os.path.exists(scripts_file_path):
    with open(scripts_file_path, 'rb') as f:
        scripts = pickle.load(f)
else:
    scripts = {}

def run_script():
    print(Fore.BLUE + "Список скриптов:")
    for i, script_name in enumerate(scripts):
        print(Fore.YELLOW + f"{i+1}. {script_name}: {scripts[script_name]}" + Style.RESET_ALL)
    choice = input(Fore.GREEN + "Выберите номер скрипта для запуска: " + Style.RESET_ALL)
    try:
        script_num = int(choice)
        script_name = list(scripts.keys())[script_num-1]
        script_relative_path = scripts[script_name]
        script_path = os.path.join(current_dir, script_relative_path)
        os.system(f"python {script_path}")
    except (ValueError, IndexError):
        print(Fore.RED + "Неверный выбор скрипта" + Style.RESET_ALL)

def show_menu():
    print(Fore.BLUE + "1. Запустить скрипт")
    print("2. Показать меню")
    print("3. Удалить скрипт")
    print("4. Выход" + Style.RESET_ALL)

def show_scripts():
    print(Fore.BLUE + "Список скриптов:")
    for script_name in scripts:
        print(Fore.YELLOW + f"{script_name}: {scripts[script_name]}" + Style.RESET_ALL)

def delete_script():
    script_name = input(Fore.GREEN + "Введите название скрипта для удаления: " + Style.RESET_ALL)
    if script_name in scripts:
        del scripts[script_name]
        with open(scripts_file_path, 'wb') as f:
            pickle.dump(scripts, f)
        print(Fore.GREEN + f"Скрипт \"{script_name}\" успешно удален" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Скрипт \"{script_name}\" не найден" + Style.RESET_ALL)

def main():
    while True:
        show_menu()
        choice = input(Fore.GREEN + "Выберите пункт меню: " + Style.RESET_ALL)
        if choice == '1':
            run_script()
        elif choice == '2':
            show_scripts()
        elif choice == '3':
            delete_script()
        elif choice == '4':
            break
        else:
            print(Fore.RED + "Неверный выбор, попробуйте еще раз" + Style.RESET_ALL)

if __name__ == '__main__':
    main()
