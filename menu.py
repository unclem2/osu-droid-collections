import os
import subprocess
from colorama import init, Fore

# Initialize colorama to support colors in the console
init()

def show_menu():
    print(Fore.CYAN + "--- MENU ---")
    print("1. Show all items")
    print("2. Run script")
    print("3. Exit")

def show_all_items():
    print(Fore.YELLOW + "--- All items ---")
    # Add logic here to display all items

def run_script(script_path):
    print(Fore.GREEN + f"--- Running script {script_path} ---")
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error executing script: {e}")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

# Dictionary with script paths
script_paths = {
    "1": "o1d-collector/1-read_collection.py",
    "2": "o1d-collector/downloader.py",
    "3": "misc/exporter.py",
    "4": "o1d-collector/jsonmerger.py",
    "5": "o1d-collector/duplicate_cleaner.py"
}

# Dictionary with script names
script_names = {
    "1": "Convert Collection",
    "2": "Map Downloader",
    "3": "Collection Exporter",
    "4": "JSON File Merger",
    "5": "Map Duplicate Cleaner"
}

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Convert script paths to relative paths
for key in script_paths:
    script_paths[key] = os.path.join(current_directory, script_paths[key])

# Main program loop
while True:
    show_menu()
    choice = input(Fore.MAGENTA + "Select an option: ")
    
    if choice == "1":
        show_all_items()
    elif choice == "2":
        print(Fore.YELLOW + "--- Available Scripts ---")
        for key in script_paths:
            print(f"{Fore.GREEN}{key}. {script_names[key]}")
        script_choice = input(Fore.MAGENTA + "Select a script: ")
        if script_choice in script_paths:
            script_path = script_paths[script_choice]
            if os.path.exists(script_path):
                run_script(script_path)
            else:
                print(Fore.RED + "The specified script was not found.")
        else:
            print(Fore.RED + "Invalid script choice.")
    elif choice == "3":
        print(Fore.YELLOW + "Exiting the program...")
        break
    else:
        print(Fore.RED + "Invalid choice. Please try again.")
