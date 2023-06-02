import os
import shutil
import re

# Получение пути к папке
path = input("Укажите путь к папке (или нажмите Enter для выбора папки, содержащей скрипт): ")
if not path:
    script_folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_folder, "Songs")
    print("Путь не указан. Выбрана папка, содержащая скрипт.")

# Функция для удаления папки с самым длинным названием
def delete_longest_folder(folder_list):
    if len(folder_list) <= 1:
        return

    longest_folder = max(folder_list, key=lambda x: len(x))
    folder_path = longest_folder
    shutil.rmtree(folder_path)
    print(f"Папка {folder_path} была удалена")

# Создание словаря с первыми 7 символами названий папок, содержащих цифры
folder_dict_7 = {}

# Проверка наличия папки "Songs"
while not os.path.exists(path):
    if path == "/":
        print("Папка 'Songs' не найдена. Скрипт завершен.")
        exit()
    path = os.path.dirname(path)

# Получение списка всех папок в папке "Songs"
folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]

# Заполнение словаря с первыми 7 символами названий папок, содержащих цифры
for folder in folders:
    folder_path = os.path.join(path, folder)
    folder_name = re.search(r'\d+', folder)
    if folder_name:
        key_7 = folder_name.group()[:7]
        if key_7 in folder_dict_7:
            folder_dict_7[key_7].append(folder_path)
        else:
            folder_dict_7[key_7] = [folder_path]

# Проверка наличия дубликатов в словаре с первыми 7 символами названий папок
duplicate_count = 0
for key_7 in folder_dict_7:
    folder_list = folder_dict_7[key_7]
    if len(folder_list) > 1:
        duplicate_count += 1
        print(f"Найдено совпадение по первым 7 символам, содержащим цифры: {key_7}")
        delete_longest_folder(folder_list)

print("Процесс завершен!")
print(f"Всего найдено дубликатов: {duplicate_count}")
