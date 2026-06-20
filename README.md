# 📂 Python File Organizer

A Python utility that automatically organizes files into categorized folders based on their file extensions. This project demonstrates file handling, automation, logging, undo functionality, and software design principles.

---

## 🚀 Features

### Basic Version

* Organizes files into categories
* Automatically creates folders
* Handles file name conflicts
* Provides organization summary
* Supports common file types

### Advanced Version

* Dry-run preview before moving files
* Logging system
* Undo last organization session
* JSON-based move history
* Extended file categories
* Conflict-free file handling
* Session tracking
* Better code modularity

---

## 📁 Supported Categories

| Category  | Extensions                                |
| --------- | ----------------------------------------- |
| Documents | pdf, doc, docx, txt, ppt, pptx, xls, xlsx |
| Images    | jpg, jpeg, png, gif, bmp, webp            |
| Videos    | mp4, mkv, avi, mov, wmv                   |
| Audio     | mp3, wav, aac, flac, ogg                  |
| Archives  | zip, rar, 7z, tar, gz                     |
| Code      | py, java, cpp, js, html, css, php         |
| Data      | csv, json, xml, yaml, sql                 |
| Others    | Any unsupported file type                 |

---

## 📂 Project Structure

```text
file-organizer/
│
├── basic/
│   └── organizer.py
│
├── advanced/
│   ├── organizer.py
│   ├── organizer.log
│   └── organizer_moves.json
│
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/file-organizer.git
```

Move into the project folder:

```bash
cd file-organizer
```

Run the program:

```bash
python organizer.py
```

---

## 💡 Example

Before:

```text
Downloads/
│
├── resume.pdf
├── vacation.jpg
├── movie.mp4
├── song.mp3
├── project.py
```

After:

```text
Downloads/
│
├── Documents/
│   └── resume.pdf
│
├── Images/
│   └── vacation.jpg
│
├── Videos/
│   └── movie.mp4
│
├── Audio/
│   └── song.mp3
│
├── Code/
│   └── project.py
```

---

## 🔄 Undo Feature (Advanced Version)

The advanced version stores move history in:

```text
organizer_moves.json
```

This allows restoring files to their original locations.

---

## 📝 Logging

All operations are logged to:

```text
organizer.log
```

Example:

```text
2026-06-20 10:25:10 | INFO | resume.pdf -> Documents
2026-06-20 10:25:12 | INFO | project.py -> Code
```

---

## 🧠 Concepts Practiced

* File Handling
* Python Modules
* OOP Principles
* Logging
* JSON Processing
* Error Handling
* Automation
* Data Structures
* Software Design

---

## 🎯 Future Improvements

### Planned Features

* Command-line interface using argparse
* Recursive folder organization
* Empty folder cleanup
* Duplicate file detection using hashes
* File size statistics
* Organization by date
* GUI using Tkinter
* Custom category configuration
* Real-time folder monitoring
* Multi-threaded processing
* Cloud storage integration
* Unit tests with pytest

### Advanced Ideas

* AI-powered file categorization
* Automatic document classification
* Duplicate image detection
* Dashboard with analytics
* Web-based interface
* Cross-platform installer

---

## 📈 Learning Outcome

This project started as a simple file organizer and evolved into a more professional utility featuring logging, undo support, session management, and safer file operations.

The goal was not only to organize files but also to practice writing maintainable and scalable Python code.

---

## 🤝 Contributions

Contributions, feature suggestions, and bug reports are welcome.

---

## 📜 License

This project is licensed under the MIT License.
