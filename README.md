# 🎵 YTDownloader

A simple Android app to search and download audio from YouTube, built with [Flet](https://flet.dev) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## 📱 Screenshots

> Coming soon

## ✨ Features

- Search songs directly from YouTube
- Download audio in m4a format
- Choose your download folder
- Remembers your last download path

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Flet](https://flet.dev) 0.81.0
- Android device (arm64-v8a recommended)

### Install dependencies

```bash
pip install flet==0.81.0 yt-dlp flet-permission-handler
```

### Run on desktop (for testing)

```bash
flet run main.py
```

### Build for Android

```bash
flet build apk --include-packages flet_permission_handler
```

The APK will be generated in the `build/` folder.

## 📁 Project Structure

```
ytdownloader/
├── assets/
│   ├── icon.png
│   └── Montserrat-VariableFont_wght.ttf
├── main.py
├── songcard.py
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## ⚠️ Disclaimer

This tool is intended for **personal and educational use only**.  
Downloading copyrighted content may violate [YouTube's Terms of Service](https://www.youtube.com/t/terms).  
The author is not responsible for any misuse of this software.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
