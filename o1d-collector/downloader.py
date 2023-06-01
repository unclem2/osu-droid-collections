import os
import concurrent.futures
import requests
import json
from urllib.parse import unquote
from tqdm import tqdm
from termcolor import colored
import threading

# Очищаем экран
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

url = "https://api.chimu.moe/v1/download/"
collections_dir = os.path.join("output", "collections")

# Создаем директорию для хранения карт
if not os.path.exists("Songs"):
    os.makedirs("Songs")

def download_beatmap(beatmap_id):
    download_url = f"{url}{beatmap_id}"
    response = requests.get(download_url)
    if response.ok:
        filename = unquote(response.headers.get('content-disposition').split('filename=')[1])
        file_path = os.path.join("Songs", filename)
        if os.path.isfile(file_path):
            print(colored(f"Карта {filename} уже существует в директории!", "yellow"))
            return
        elif os.path.isdir(os.path.join("Songs", filename.split('.')[0])):
            print(colored(f"Папка {filename.split('.')[0]} уже существует в директории!", "yellow"))
            return
        with open(file_path, 'wb') as f:
            f.write(response.content)
            if os.path.isfile(file_path):
                print(colored(f"Карта {filename} успешно загружена!", "green"))
            else:
                print(colored(f"Ошибка записи карты {filename} на диск!", "red"))
    else:
        print(colored(f"Ошибка загрузки карты с ID {beatmap_id}: {response.status_code}", "red"))

# Получаем список доступных коллекций
collections = []
for file in os.listdir(collections_dir):
    file_path = os.path.join(collections_dir, file)
    if os.path.isfile(file_path) and "beatmapset_ids_" in file:
        collection_name = file.replace("beatmapset_ids_", "").replace(".json", "")
        collections.append(collection_name)

# Выводим список коллекций и просим пользователя выбрать
print(colored("Доступные коллекции:", "cyan"))
for i, collection in enumerate(collections):
    print(colored(f"{i + 1}. {collection}", "cyan"))

selected_collection = None
while selected_collection is None:
    try:
        choice = int(input(colored("Выберите номер коллекции для загрузки: ", "yellow")))
        if 1 <= choice <= len(collections):
            selected_collection = collections[choice - 1]
        else:
            print(colored("Некорректный выбор. Попробуйте снова.", "red"))
    except ValueError:
        print(colored("Некорректный выбор. Попробуйте снова.", "red"))

# Загружаем выбранную коллекцию
collection_file = os.path.join(collections_dir, f"beatmapset_ids_{selected_collection}.json")
with open(collection_file, 'r') as f:
    data = json.load(f)
    if isinstance(data, list):
        print(colored(f"Загружаем коллекцию: {selected_collection}", "green"))

        stop_event = threading.Event()  # Событие для остановки загрузки

        def check_user_input():
            input("Нажмите Enter для остановки загрузки...")
            stop_event.set()  # Установка события остановки

        # Запускаем поток для проверки ввода пользователя
        input_thread = threading.Thread(target=check_user_input)
        input_thread.start()

        with tqdm(total=len(data), position=0, dynamic_ncols=True) as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for beatmap_id in data:
                    if stop_event.is_set():
                        break  # Прерываем цикл загрузки, если событие остановки установлено
                    future = executor.submit(download_beatmap, beatmap_id)
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures):
                    pbar.update(1)

        # Ожидаем завершения потока проверки ввода
        input_thread.join()

    else:
        print(colored(f"Ошибка: Файл '{collection_file}' не содержит список beatmap IDs.", "red"))

print(colored("Скрипт завершен.", "cyan"))
