import requests
import json
from tqdm import tqdm
from termcolor import colored

name = "name1"  # название коллекции(collection name)
k = "f9609716f769c97b6d02603570b1c95cab912593"  # osu!api key  https://osu.ppy.sh/home/account/edit#legacy-api

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

print(colored("Loading hashes from file 'hashes.json'...", "blue"))
with open("hashes.json", "r") as f:
    hashes = json.load(f)

beatmapset_infos = []
beatmapset_ids = []
print(colored("Getting beatmapset info...", "blue"))
for hash in tqdm(hashes, desc=colored("Getting Beatmapset Info", "cyan")):
    beatmapset_info = get_beatmapset_info(hash)
    if beatmapset_info is not None:
        beatmapset_infos.append(beatmapset_info)
        beatmapset_id = beatmapset_info['beatmapset_id']
        if beatmapset_id not in beatmapset_ids:
            beatmapset_ids.append(beatmapset_id)

print(colored(f"Got {len(beatmapset_infos)} beatmapset infos for {len(beatmapset_ids)} beatmapset IDs.", "green"))
print(colored(f"Writing beatmapset IDs to file 'beatmapset_ids.json': {beatmapset_ids}", "blue"))
with open("beatmapset_ids.json", "w") as f:
    json.dump(beatmapset_ids, f)

beatmapset_list = []
print(colored("Creating beatmapset list...", "blue"))
for info in beatmapset_infos:
    beatmapset_id = info['beatmapset_id']
    artist = info['artist'].replace("[", "").replace("]", "")
    title = info['title']
    beatmapset_list.append(f"{beatmapset_id} {artist} - {title}")

beatmapset_list = list(set(beatmapset_list))

print(colored(f"Writing beatmapset list to file 'beatmapset_list.json' for collection '{name}': {beatmapset_list}", "blue"))
with open("beatmapset_list.json", "w") as f:
    json.dump({name: beatmapset_list}, f, indent=4)

print(colored("Beatmapset List:", "green"), beatmapset_list)
print(colored("Beatmapset IDs:", "green"), beatmapset_ids)
