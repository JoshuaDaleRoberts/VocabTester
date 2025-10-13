import webbrowser
from pathlib import Path

import pickle

file_path = Path("index.html").resolve()
webbrowser.open(file_path.as_uri(), new=2)

items = ["Level 1", "personal","Level 3"]

with open("items.pkl", "wb") as f:
    pickle.dump(items, f)


b = list()

with open("items.pkl", "rb") as f:
    b = pickle.load(f)

html_path = Path("index.html")
temp_path = Path("temp.html")
html = html_path.read_text(encoding="utf-8")

li_items = "\n".join(f"<li>\n{item}\n <button type='button'>Edit</button></li>" for item in b)

html = html.replace("<!-- ITEMS -->", li_items)
temp_path.write_text(html, encoding="utf-8")
webbrowser.open(temp_path.resolve().as_uri(), new=2)
