# check_env.py

packages = [
    ("Flask", "flask"),
    ("google-generativeai", "google.generativeai"),
    ("gspread", "gspread"),
    ("oauth2client", "oauth2client"),
    ("SpeechRecognition", "speech_recognition"),
    ("pydub", "pydub"),
    ("gTTS", "gtts"),
    ("Werkzeug", "werkzeug"),
    ("Pillow", "PIL")
]

for name, module in packages:
    try:
        __import__(module)
        print(f"[✔] {name} is installed")
    except ImportError:
        print(f"[✖] {name} is NOT installed")
