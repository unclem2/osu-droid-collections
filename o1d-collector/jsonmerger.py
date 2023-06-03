import os
import json

def merge_favorite_scripts(root_directory):
    data = {}
    file_paths = []  # Список путей к объединяемым файлам
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file == "favorite.json":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    favorite_data = json.load(f)
                    data.update(favorite_data)
                file_paths.append(file_path)  # Добавляем путь к файлу в список
    return data, file_paths

# Получаем текущую директорию скрипта
script_directory = os.path.dirname(os.path.abspath(__file__))

# Определяем корневую директорию как папку ниже текущей директории скрипта
root_directory = os.path.join(script_directory, "..", "..")

# Вызываем функцию для объединения скриптов и получения путей файлов
merged_data, file_paths = merge_favorite_scripts(root_directory)

# Выводим пути файлов, которые будут объединены
print("Обнаружены следующие файлы для объединения:")
for file_path in file_paths:
    print(file_path)

# Подтверждение сохранения файла
confirm = input("Хотите сохранить объединенный файл? (yes/no): ")
if confirm.lower() == "yes":
    # Ввод пути для сохранения файла 
    save_directory = root_directory
    save_path = os.path.join(save_directory, 'json', "merged_favorite.json")

    # Записываем объединенные данные в новый файл
    with open(save_path, 'w') as merged_file:
        json.dump(merged_data, merged_file, indent=4)
    print("Файл успешно сохранен по пути:", save_path)
else:
    print("Сохранение отменено.")
