import os
import concurrent.futures
import requests
import json
from urllib.parse import unquote
from tqdm import tqdm
from termcolor import colored
import threading

# Clear the screen
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

url = "https://api.chimu.moe/v1/download/"
collections_dir = os.path.join("output", "collections")

def find_songs_directory(directory):
    for root, dirs, files in os.walk(directory):
        if "Songs" in dirs:
            return os.path.join(root, "Songs")
    return None

# Determine the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Search for the "Songs" folder two levels above the script directory
parent_directory = os.path.abspath(os.path.join(script_directory, ".."))
songs_dir = find_songs_directory(parent_directory)
if songs_dir is None:
    parent_directory = os.path.abspath(os.path.join(parent_directory, ".."))
    songs_dir = find_songs_directory(parent_directory)

# Create the "Songs" folder if not found
if songs_dir is None:
    songs_dir = os.path.join(parent_directory, "Songs")
    os.makedirs(songs_dir)

def download_beatmap(beatmap_id):
    download_url = f"{url}{beatmap_id}"
    response = requests.get(download_url)
    if response.ok:
        filename = unquote(response.headers.get('content-disposition').split('filename=')[1])
        file_path = os.path.join(songs_dir, filename)
        if os.path.isfile(file_path):
            print(colored(f"The beatmap {filename} already exists in the directory!", "yellow"))
            return
        elif os.path.isdir(os.path.join(songs_dir, filename.split('.')[0])):
            print(colored(f"The folder {filename.split('.')[0]} already exists in the directory!", "yellow"))
            return
        with open(file_path, 'wb') as f:
            f.write(response.content)
            if os.path.isfile(file_path):
                print(colored(f"The beatmap {filename} was successfully downloaded!", "green"))
            else:
                print(colored(f"Failed to write the beatmap {filename} to disk!", "red"))
    else:
        print(colored(f"Failed to download beatmap with ID {beatmap_id}: {response.status_code}", "red"))

# Get the list of available collections
collections = []
for file in os.listdir(collections_dir):
    file_path = os.path.join(collections_dir, file)
    if os.path.isfile(file_path) and "beatmapset_ids_" in file:
        collection_name = file.replace("beatmapset_ids_", "").replace(".json", "")
        collections.append(collection_name)

# Display the list of collections and prompt the user to choose
print(colored("Available collections:", "cyan"))
for i, collection in enumerate(collections):
    print(colored(f"{i + 1}. {collection}", "cyan"))

selected_collection = None
while selected_collection is None:
    try:
        choice = int(input(colored("Select the collection number to download: ", "yellow")))
        if 1 <= choice <= len(collections):
            selected_collection = collections[choice - 1]
        else:
            print(colored("Invalid choice. Please try again.", "red"))
    except ValueError:
        print(colored("Invalid choice. Please try again.", "red"))

# Download the selected collection
collection_file = os.path.join(collections_dir, f"beatmapset_ids_{selected_collection}.json")
with open(collection_file, 'r') as f:
    data = json.load(f)
    if isinstance(data, list):
        print(colored(f"Downloading collection: {selected_collection}", "green"))

        stop_event = threading.Event()  # Event for stopping the download

        def check_user_input():
            while True:
                if input() or stop_event.is_set():
                    break
            stop_event.set()  # Set the stop event

        # Start a thread to check user input
        input_thread = threading.Thread(target=check_user_input)
        input_thread.start()

        with tqdm(total=len(data), position=0, dynamic_ncols=True) as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for beatmap_id in data:
                    if stop_event.is_set():
                        break  # Break the download loop if the stop event is set
                    future = executor.submit(download_beatmap, beatmap_id)
                    futures.append(future)

                completed = 0
                for future in concurrent.futures.as_completed(futures):
                    pbar.update(1)
                    completed += 1
                    if completed >= len(futures):
                        stop_event.set()  # Set the stop event after completing all tasks

        # Wait for the input thread to finish
        input_thread.join()

    else:
        print(colored(f"Error: The file '{collection_file}' does not contain a list of beatmap IDs.", "red"))

print(colored("Script completed.", "cyan"))
