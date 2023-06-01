import buffer
import requests
import json
import os
import sys
from termcolor import colored
import stat
import subprocess

OUTPUT_DIR = "output/hashes"  # Название папки для сохранения вывода

def collection_to_dict(filename):
    collections = {}
    try:
        with open(filename, "rb") as db:
            collections["version"] = buffer.read_uint(db)
            collections["num_collections"] = buffer.read_uint(db)
            collections["collections"] = []
            for i in range(collections["num_collections"]):
                collection = {}
                collection["name"] = buffer.read_string(db)
                collection["size"] = buffer.read_uint(db)
                collection["hashes"] = []
                for i in range(collection["size"]):
                    collection["hashes"].append(buffer.read_string(db))
                collections["collections"].append(collection)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, "hashes.json")

        with open(output_path, "w") as f:
            json.dump(collections, f, indent=2)
            print(colored(f"Output saved to: {output_path}", "green"))

        os.chmod(OUTPUT_DIR, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # Установка разрешений для папки
    except Exception as e:
        print(colored("Error:", "red"), colored(e, "red"))

    return collections

if __name__ == "__main__":
    db_files = [f for f in os.listdir() if f.endswith(".db")]
    if len(db_files) == 0:
        print(colored("Error:", "red"), "No .db files found in the current directory.")
    elif len(db_files) == 1:
        db_file = db_files[0]
        print(colored("Processing collection file:", "blue"), db_file)
        print(json.dumps(collection_to_dict(db_file), indent=2))
    else:
        print(colored("Multiple .db files found in the current directory. Please select the file to process:", "yellow"))
        for i, db_file in enumerate(db_files):
            print(f"{i+1}. {db_file}")
        while True:
            choice = input("Enter the number of the file to process (or 'q' to quit): ")
            if choice.lower() == "q":
                sys.exit()
            try:
                choice = int(choice)
                if 1 <= choice <= len(db_files):
                    db_file = db_files[choice-1]
                    print(colored("Processing collection file:", "blue"), db_file)
                    print(json.dumps(collection_to_dict(db_file), indent=2))
                    break
                else:
                    print(colored("Invalid choice. Please enter a valid number.", "red"))
            except ValueError:
                print(colored("Invalid choice. Please enter a valid number.", "red"))



# Определяем путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к файлу, который нужно запустить
script_path = os.path.join(current_dir, "2-create_collection.py")

# Запускаем другой код
subprocess.call(["python", script_path])

# Код, который будет выполняться после завершения другого кода
print("Запуск другого кода завершен")
