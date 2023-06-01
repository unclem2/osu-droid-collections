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

# Ввод пути к корневой директории через консоль
root_directory = input("Введите путь к корневой директории: ")

# Вызываем функцию для объединения скриптов и получения путей файлов
merged_data, file_paths = merge_favorite_scripts(root_directory)

# Выводим пути файлов, которые будут объединены
print("Обнаружены следующие файлы для объединения:")
for file_path in file_paths:
    print(file_path)

# Подтверждение сохранения файла
confirm = input("Хотите сохранить объединенный файл? (yes/no): ")
if confirm.lower() == "yes":
    # Ввод пути для сохранения файла через консоль
    save_directory = input("Введите путь для сохранения файла: ")
    save_path = os.path.join(save_directory, "merged_favorite.json")

    # Записываем объединенные данные в новый файл
    with open(save_path, 'w') as merged_file:
        json.dump(merged_data, merged_file, indent=4)
    print("Файл успешно сохранен по пути:", save_path)
else:
    print("Сохранение отменено.")
