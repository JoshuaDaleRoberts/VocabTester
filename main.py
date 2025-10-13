import webbrowser
from pathlib import Path

file_path = Path("index.html").resolve()
webbrowser.open(file_path.as_uri(), new=2)