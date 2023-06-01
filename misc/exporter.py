import os
import shutil

# Определяем путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath(os.path.join(current_dir, '..', 'output'))
collections_dir = os.path.join(output_dir, 'collections')
misc_dir = os.path.join(current_dir, '..')

def move_collection():
    print("Список доступных коллекций:")
    collections = []
    for filename in os.listdir(collections_dir):
        if filename.endswith(".json") and "beatmapset_ids" not in filename:
            collection_name = os.path.splitext(filename)[0]
            if "beatmapset_list_" in collection_name:
                collection_name = collection_name.replace("beatmapset_list_", "")
            collections.append((collection_name, filename))
            print(collection_name)
    
    if not collections:
        print("Нет доступных коллекций для перемещения.")
        return
    
    choice = input("Выберите коллекцию для перемещения: ")
    
    selected_collection = None
    for collection_name, filename in collections:
        if collection_name == choice:
            selected_collection = filename
            break
    
    if not selected_collection:
        print("Неверный выбор коллекции.")
        return
    
    source_path = os.path.join(collections_dir, selected_collection)
    destination_path = os.path.join(misc_dir, "favorite.json")
    
    try:
        shutil.move(source_path, destination_path)
        print("Коллекция успешно перемещена в папку 'misc' и переименована в 'favorite.json'.")
    except Exception as e:
        print(f"Ошибка при перемещении коллекции: {e}")

# Вызываем функцию для перемещения коллекции
move_collection()
