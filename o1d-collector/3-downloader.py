import os

# Очищаем экран
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

# Остальной код
import requests
import json
from urllib.parse import unquote
from tqdm import tqdm
from termcolor import colored

url = "https://api.chimu.moe/v1/download/"
json_file = "beatmapset_ids.json"

# Создаем директорию для хранения карт
if not os.path.exists("Songs"):
    os.makedirs("Songs")

with open(json_file, 'r') as f:
    data = json.load(f)
    with tqdm(total=len(data), position=0, dynamic_ncols=True) as pbar:
        for beatmap_id in data:
            download_url = f"{url}{beatmap_id}"
            response = requests.get(download_url)
            if response.ok:
                filename = unquote(response.headers.get('content-disposition').split('filename=')[1])
                file_path = os.path.join("Songs", filename)
                if os.path.isfile(file_path):
                    pbar.write(colored(f"Карта {filename} уже существует в директории!", "yellow"))
                    continue
                elif os.path.isdir(os.path.join("Songs", filename.split('.')[0])):
                    pbar.write(colored(f"Папка {filename.split('.')[0]} уже существует в директории!", "yellow"))
                    continue
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    if os.path.isfile(file_path):
                        pbar.write(colored(f"Карта {filename} успешно загружена!", "green"))
                    else:
                        pbar.write(colored(f"Ошибка записи карты {filename} на диск!", "red"))
            else:
                pbar.write(colored(f"Ошибка загрузки карты с ID {beatmap_id}: {response.status_code}", "red"))
            pbar.update(1)
