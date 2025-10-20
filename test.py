import http.server
import socketserver
from urllib.parse import parse_qs
import pickle
from urllib.parse import urlparse
port = 2704
Handler = http.server.SimpleHTTPRequestHandler

from http.server import HTTPServer, BaseHTTPRequestHandler

# Define a simple class to hold vocab items
class Vocab():
    def __init__(self, name):
        self.name = name


# Functions to read and write the class list to a file
def write_to_file():
    with open("items.pkl", "wb") as f:
        pickle.dump(classList, f)

# Function to read the class list from a file
def read_from_file():
    with open("items.pkl", "rb") as f:
        a = pickle.load(f)
        return a

# Initialize the class list, but grab from file if it exists
try:
    classList = read_from_file()
except FileNotFoundError:
    classList = []
    pickle.dump(classList, open("items.pkl", "wb"))

# Function to generate HTML list items from the class list
def make_html_list():
    classList = read_from_file()
    text = ""
    for i in range(len(classList)):
        name = classList[i].name
        text += f""" 
        <li>
            <a href="/class?{i}">{name}</a>
            <form method="post" action="/" onsubmit="return confirm('Are you sure you want to delete this class?');">
                <input type="hidden" name="action" value="delete">
                <input type="hidden" name="id" value="{i}">
                <button type="submit">Delete</button>
            </form>
        </li>
        """
    return text

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = urlparse(self.path)
        if page.path == "/class":
            with open("class.html", "rb") as f:
                html = f.read()
            class_number = page.query
            class_name = classList[int(class_number)].name
            html = html.replace(b"<!-- c -->", class_name.encode('utf-8'))
        else: 
            with open("index.html", "rb") as f:
                html = f.read()
            html = html.replace(b"<!-- ITEMS -->", make_html_list().encode('utf-8'))
            
        self.wfile.write(html)
        
    def do_POST(self):
        # Parse the form data posted
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))
        action = data.get("action", [""])[0]
        # Add Vocab
        if action == "add":
            vocab_value = data.get("vocab", [None])[0]
            a = Vocab(vocab_value)
            classList.append(a)
            write_to_file()
        # Delete Vocab
        if action == "delete":
            id_value = int(data.get("id", [-1])[0])
            classList.pop(id_value)
            write_to_file()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("index.html", "rb") as f:
          html = f.read()
          html = html.replace(b"<!-- ITEMS -->", make_html_list().encode('utf-8'))
          self.wfile.write(html)

if __name__ == "__main__":
    server = HTTPServer(('localhost', port), SimpleHandler)
    print(f"Server running on http://localhost:{port}")
    server.serve_forever()

