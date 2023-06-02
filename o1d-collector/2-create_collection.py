import requests
import json
import os
import stat
from tqdm import tqdm
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

def get_api_key():
    with open("api_key.txt", "r") as f:
        return f.read().strip()

k = get_api_key()

def get_beatmapset_info(hash):
    url = f"https://osu.ppy.sh/api/get_beatmaps?k={k}&h={hash}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            beatmapset_info = {
                "beatmapset_id": data[0]['beatmapset_id'],
                "artist": data[0]['artist'],
                "title": data[0]['title']
            }
            return beatmapset_info
    return None

# Остальной код остается неизменным


def process_category(category):
    name = category["name"]
    hashes = category["hashes"]

    print(colored(f"Processing category: {name}", "blue"))

    beatmapset_infos = []
    beatmapset_ids = []

    print(colored("Getting beatmapset info...", "blue"))
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_beatmapset_info, hash) for hash in hashes]
        for future in tqdm(futures, total=len(hashes), desc=colored("Getting Beatmapset Info", "cyan")):
            beatmapset_info = future.result()
            if beatmapset_info is not None:
                beatmapset_infos.append(beatmapset_info)
                beatmapset_id = beatmapset_info['beatmapset_id']
                if beatmapset_id not in beatmapset_ids:
                    beatmapset_ids.append(beatmapset_id)

    print(colored(f"Got {len(beatmapset_infos)} beatmapset infos for {len(beatmapset_ids)} beatmapset IDs.", "green"))
    output_dir = os.path.join("output", "collections")
    os.makedirs(output_dir, exist_ok=True)
    os.chmod(output_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # Set permissions to 755
    beatmapset_ids_file = os.path.join(output_dir, f"beatmapset_ids_{name}.json")
    print(colored(f"Writing beatmapset IDs to file '{beatmapset_ids_file}': {beatmapset_ids}", "blue"))
    with open(beatmapset_ids_file, "w") as f:
        json.dump(beatmapset_ids, f)

    beatmapset_list = []
    print(colored("Creating beatmapset list...", "blue"))
    for info in beatmapset_infos:
        beatmapset_id = info['beatmapset_id']
        artist = info['artist'].replace("[", "").replace("]", "")
        title = info['title']
        beatmapset_list.append(f"{beatmapset_id} {artist} - {title}")

    beatmapset_list = list(set(beatmapset_list))

    beatmapset_list_file = os.path.join(output_dir, f"beatmapset_list_{name}.json")
    print(colored(f"Writing beatmapset list to file '{beatmapset_list_file}' for collection '{name}': {beatmapset_list}", "blue"))
    with open(beatmapset_list_file, "w") as f:
        json.dump({name: beatmapset_list}, f, indent=4)

    print(colored(f"Processed category: {name}", "blue"))
    print(colored("Beatmapset List:", "green"), beatmapset_list)
    print(colored("Beatmapset IDs:", "green"), beatmapset_ids)

output_hashes_dir = os.path.join("output", "hashes")
hashes_file = os.path.join(output_hashes_dir, "hashes.json")
print(colored(f"Loading categories from file '{hashes_file}'...", "blue"))
with open(hashes_file, "r") as f:
    data = json.load(f)
    categories = data["collections"]

for category in categories:
    process_category(category)
