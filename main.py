import webbrowser
from pathlib import Path

file_path = Path("index.html").resolve()
webbrowser.open(file_path.as_uri(), new=2)

items = ["1st Period", "2nd Period", "3rd Period", "4th Period", "5th Period", "6th Period", "7th Period"]

html_path = Path("index.html")
temp_path = Path("temp.html")
html = html_path.read_text(encoding="utf-8")

li_items = "\n".join(f"    <li>\n        {item}\n    </li>" for item in items)

html = html.replace("<!-- ITEMS -->", li_items)
temp_path.write_text(html, encoding="utf-8")
webbrowser.open(temp_path.resolve().as_uri(), new=2)
