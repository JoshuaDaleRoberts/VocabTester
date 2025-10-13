print("Hello World")
import webbrowser
import os
f = open("index.html", "w")

file_path = os.path.abspath("index.html")
webbrowser.open(f"file://{file_path}")


