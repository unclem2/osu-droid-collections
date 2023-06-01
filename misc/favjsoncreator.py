from tkinter import Tk
from tkinter import filedialog
from pathlib import Path
import json

root = Tk()
root.withdraw()
folder_path = filedialog.askdirectory()
if not folder_path:
    print("Отменено пользователем.")
    exit()
folder_path = Path(folder_path)
try:
    # Получаем список папок в директории
    folder_list = [folder.name for folder in folder_path.iterdir() if folder.is_dir()]
    # Создаем словарь с именами папок
    data = {"folder_names": folder_list}
    # Открываем диалоговое окно для выбора места сохранения файла
    save_path = filedialog.asksaveasfilename(defaultextension=".json")
    if not save_path:
        print("Отменено пользователем.")
        exit()
    # Открываем файл для записи
    with open(save_path, "w") as file:
        # Записываем словарь в формате JSON в файл
        json.dump(data, file, indent=4)
    print(f"Список папок успешно сохранен в файле {save_path}")
except OSError as e:
    print(f"Ошибка: {e.strerror}")