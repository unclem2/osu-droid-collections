import json
from tkinter import Tk, filedialog
# Открываем диалоговое окно для выбора первого файла
root = Tk()
root.withdraw()
file_path1 = filedialog.askopenfilename(title='Выберите первый файл')
# Загружаем содержимое первого файла в переменную data1
with open(file_path1, 'r') as file1:
    data1 = json.load(file1)
# Открываем диалоговое окно для выбора второго файла
file_path2 = filedialog.askopenfilename(title='Выберите второй файл')
# Загружаем содержимое второго файла в переменную data2
with open(file_path2, 'r') as file2:
    data2 = json.load(file2)
# Объединяем два словаря в один
data = {**data1, **data2}
# Открываем диалоговое окно для выбора места сохранения объединенного файла
save_path = filedialog.asksaveasfilename(title='Выберите место сохранения файла', defaultextension='.json')
# Записываем объединенные данные в новый файл
with open(save_path, 'w') as merged_file:
    json.dump(data, merged_file, indent=4)