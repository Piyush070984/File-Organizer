import os
import shutil
import json
import logging
from datetime import datetime
from collections import defaultdict

# ----------------------------
# File categories
# ----------------------------
FILE_CATEGORIES = {
    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".odt", ".rtf"
    },
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff"
    },
    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"
    },
    "Audio": {
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"
    },
    "Archives": {
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"
    },
    "Code": {
        ".py", ".ipynb", ".java", ".cpp", ".c", ".h", ".hpp", ".js", ".ts",
        ".html", ".css", ".php", ".go", ".rs", ".swift", ".kt", ".sh"
    },
    "Data": {
        ".csv", ".json", ".xml", ".yaml", ".yml", ".sql", ".parquet"
    },
}

OTHER_CATEGORY = "Others"
LOG_FILE_NAME = "organizer.log"
UNDO_FILE_NAME = "organizer_moves.json"


# ----------------------------
# Helpers
# ----------------------------
def setup_logger(folder_path: str) -> logging.Logger:
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if function called multiple times
    if logger.handlers:
        return logger

    log_path = os.path.join(folder_path, LOG_FILE_NAME)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return OTHER_CATEGORY


def load_undo_data(undo_file_path: str):
    if not os.path.exists(undo_file_path):
        return []
    try:
        with open(undo_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_undo_data(undo_file_path: str, data):
    with open(undo_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def resolve_name_conflict(path: str) -> str:
    """
    If path exists, create file(1).ext, file(2).ext, etc.
    """
    if not os.path.exists(path):
        return path

    directory, filename = os.path.split(path)
    base, ext = os.path.splitext(filename)
    counter = 1

    while True:
        candidate = os.path.join(directory, f"{base}({counter}){ext}")
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def get_all_category_folder_names():
    return set(FILE_CATEGORIES.keys()) | {OTHER_CATEGORY}


# ----------------------------
# Main organize function
# ----------------------------
def organize_folder(folder_path: str, dry_run: bool = True):
    if not os.path.isdir(folder_path):
        print("❌ Invalid folder path.")
        return

    logger = setup_logger(folder_path)
    undo_file_path = os.path.join(folder_path, UNDO_FILE_NAME)

    summary = defaultdict(int)
    planned_moves = []

    ignore_folders = get_all_category_folder_names()

    # Collect planned moves first
    for item in os.listdir(folder_path):
        source_path = os.path.join(folder_path, item)

        # Skip directories
        if os.path.isdir(source_path):
            # Explicit skip for already organized category folders
            if item in ignore_folders:
                continue
            # Skip all directories in basic mode
            continue

        # Skip own metadata files
        if item in {LOG_FILE_NAME, UNDO_FILE_NAME}:
            continue

        _, ext = os.path.splitext(item)
        category = get_category(ext)
        destination_dir = os.path.join(folder_path, category)
        destination_path = os.path.join(destination_dir, item)
        destination_path = resolve_name_conflict(destination_path)

        planned_moves.append((item, source_path, destination_path, category))

    if not planned_moves:
        print("ℹ️ No files to organize.")
        return

    # Dry-run preview
    print("\n--- Dry Run Preview ---")
    for item, source, destination, category in planned_moves:
        print(f"{item} -> {category}/ ({os.path.basename(destination)})")
    print("-----------------------")

    if dry_run:
        choice = input("Proceed with moving these files? (y/n): ").strip().lower()
        if choice != "y":
            print("❎ Operation cancelled.")
            return

    # Execute moves
    move_records = []
    total_moved = 0

    for item, source, destination, category in planned_moves:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)

        summary[category] += 1
        total_moved += 1

        move_record = {
            "timestamp": datetime.now().isoformat(),
            "file": item,
            "from": source,
            "to": destination,
            "category": category
        }
        move_records.append(move_record)

        logger.info(f"{item} -> {category} | {source} -> {destination}")

    # Save undo history (append session)
    undo_data = load_undo_data(undo_file_path)
    undo_data.append({
        "session_timestamp": datetime.now().isoformat(),
        "moves": move_records
    })
    save_undo_data(undo_file_path, undo_data)

    # Print summary
    print(f"\n✅ {total_moved} files organized.\n")
    for category in sorted(summary.keys()):
        print(f"{summary[category]} {category}")

    print(f"\n📝 Log file: {os.path.join(folder_path, LOG_FILE_NAME)}")
    print(f"↩️ Undo data: {undo_file_path}")


# ----------------------------
# Undo last session
# ----------------------------
def undo_last(folder_path: str):
    undo_file_path = os.path.join(folder_path, UNDO_FILE_NAME)
    logger = setup_logger(folder_path)

    undo_data = load_undo_data(undo_file_path)
    if not undo_data:
        print("ℹ️ Nothing to undo.")
        return

    last_session = undo_data[-1]
    moves = last_session.get("moves", [])

    if not moves:
        print("ℹ️ Last session has no moves.")
        return

    restored = 0

    # Reverse order to reduce collision chances
    for record in reversed(moves):
        src = record["to"]    # current location
        dst = record["from"]  # original location

        if not os.path.exists(src):
            logger.warning(f"UNDO SKIP (missing): {src}")
            continue

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        dst_final = resolve_name_conflict(dst)
        shutil.move(src, dst_final)
        restored += 1

        logger.info(f"UNDO | {src} -> {dst_final}")

    # Remove last undo session after successful attempt
    undo_data.pop()
    save_undo_data(undo_file_path, undo_data)

    print(f"↩️ Undo complete. Restored {restored} files.")


# ----------------------------
# CLI
# ----------------------------
def main():
    print("File Organizer")
    print("1) Organize files")
    print("2) Undo last organize session")
    choice = input("Choose an option (1/2): ").strip()

    folder_path = input("Enter folder path: ").strip()

    if choice == "1":
        dry_choice = input("Enable dry run mode? (y/n, recommended y): ").strip().lower()
        dry_run = (dry_choice == "y")
        organize_folder(folder_path, dry_run=dry_run)
    elif choice == "2":
        undo_last(folder_path)
    else:
        print("❌ Invalid option.")


if __name__ == "__main__":
    main()