import os
import shutil
from collections import defaultdict

# Extension categories
FILE_CATEGORIES = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}

def get_category(extension: str) -> str:
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

def organize_folder(folder_path: str):
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    summary = defaultdict(int)
    total_moved = 0

    # List only files in the top-level folder
    for item in os.listdir(folder_path):
        source_path = os.path.join(folder_path, item)

        if not os.path.isfile(source_path):
            continue  # Skip directories

        _, ext = os.path.splitext(item)
        ext = ext.lower()

        category = get_category(ext)
        destination_dir = os.path.join(folder_path, category)
        destination_path = os.path.join(destination_dir, item)

        # Create destination folder if not exists
        os.makedirs(destination_dir, exist_ok=True)

        # Handle name conflict by renaming
        counter = 1
        base_name, file_ext = os.path.splitext(item)
        while os.path.exists(destination_path):
            new_name = f"{base_name}({counter}){file_ext}"
            destination_path = os.path.join(destination_dir, new_name)
            counter += 1

        shutil.move(source_path, destination_path)
        summary[category] += 1
        total_moved += 1

    # Print summary
    print(f"\n✅ {total_moved} files organized.\n")
    for category in sorted(summary.keys()):
        print(f"{summary[category]} {category}")

if __name__ == "__main__":
    path = input("Enter folder path to organize: ").strip()
    organize_folder(path)