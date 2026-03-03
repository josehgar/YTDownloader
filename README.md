# 🎵 YTDownloader

A simple Android app to search and download audio from YouTube, built with [Flet](https://flet.dev) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## 📱 Screenshots

Main screen


<img width="485" height="708" alt="image" src="https://github.com/user-attachments/assets/0fdaa74e-62a2-4327-9357-32d5a7c05962" />

Main screen with search


<img width="480" height="721" alt="image" src="https://github.com/user-attachments/assets/69e1c1fd-d4aa-4699-8d46-8887b3d56ab5" />

Downloading a song


<img width="476" height="645" alt="image" src="https://github.com/user-attachments/assets/d2c83c16-15e6-493a-af62-a858f18e5b64" />


## ✨ Features

- Search songs directly from YouTube
- Download audio in m4a format
- Choose your download folder
- Data storage such as download path using JSON

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Flet](https://flet.dev) 0.81.0
- Android device (arm64-v8a recommended)

### Install dependencies

```bash
pip install flet yt-dlp flet-permission-handler
```

### Run on desktop (for testing)

```bash
flet run main.py
```

### Problems with libraries?

If your IDE doesn't detect the libraries, execute this lines to generate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

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

## 🔰 Adittional information

I am a 2th grade software engineering student and this is my first serious project. Any contribution will be appreciated.

