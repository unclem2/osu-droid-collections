import os
import shutil
from tkinter import filedialog

# Выберите путь к папке, которую нужно проверить
path = filedialog.askdirectory()

# Проверьте, существует ли папка "duplicates", и если она не существует, создайте ее
if not os.path.exists(os.path.join(path, "duplicates")):
    os.makedirs(os.path.join(path, "duplicates"))

# Получите список всех папок в указанной директории
folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]

# Создайте словарь, в котором ключ - первые 7 символов названия папки, а значение - список папок с таким названием
folder_dict = {}
for folder in folders:
    key = folder[:7]
    if key in folder_dict:
        folder_dict[key].append(folder)
    else:
        folder_dict[key] = [folder]

# Пройдитесь по каждой паре папок с одинаковым названием и переместите ту, которая короче, в папку "duplicates"
for key in folder_dict:
    if len(folder_dict[key]) > 1:
        shortest_folder = min(folder_dict[key], key=len)
        for folder in folder_dict[key]:
            if folder == shortest_folder:
                shutil.move(os.path.join(path, folder), os.path.join(path, "duplicates", folder))
                print(f"Папка {folder} была перемещена в папку duplicates")

print("Процесс завершен!")