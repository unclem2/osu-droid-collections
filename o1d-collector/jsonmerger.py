import os
import json

def merge_favorite_scripts(root_directory):
    data = {}
    file_paths = []  # List of paths to the merged files
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file == "favorite.json":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    favorite_data = json.load(f)
                    data.update(favorite_data)
                file_paths.append(file_path)  # Add the file path to the list
    return data, file_paths

# Get the current script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Set the root directory as a folder below the current script directory
root_directory = os.path.join(script_directory, "..", "..")

# Call the function to merge scripts and get the file paths
merged_data, file_paths = merge_favorite_scripts(root_directory)

# Display the file paths that will be merged
print("The following files will be merged:")
for file_path in file_paths:
    print(file_path)

# Confirm file saving
confirm = input("Do you want to save the merged file? (yes/no): ")
if confirm.lower() == "yes":
    # Enter the save path for the file
    save_directory = root_directory
    save_path = os.path.join(save_directory, 'json', "merged_favorite.json")

    # Write the merged data to a new file
    with open(save_path, 'w') as merged_file:
        json.dump(merged_data, merged_file, indent=4)
    print("File successfully saved at:", save_path)
else:
    print("Save canceled.")
