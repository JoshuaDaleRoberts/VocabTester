import http.server
import socketserver
from urllib.parse import parse_qs
import pickle
port = 2704
Handler = http.server.SimpleHTTPRequestHandler

from http.server import HTTPServer, BaseHTTPRequestHandler

class Vocab():
    def __init__(self, name):
        self.name = name


def write_to_file():
    print("Writing to file")
    with open("items.pkl", "wb") as f:
        pickle.dump(classList, f)
        print(str(classList))

def read_from_file():
    print("Reading from file")
    with open("items.pkl", "rb") as f:
        a = pickle.load(f)
        return a

classList = read_from_file()

def make_html_list():
    classList = read_from_file()
    text = ""
    for i in range(len(classList)):
        name = classList[i].name
        text += f""" 
        <li>
            <p>{name}</p>
            <form method="post" action="/">
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
        with open("index.html", "rb") as f:
          html = f.read()
        #   html = html.replace(b"<!-- ITEMS -->", b"\n".join(f"<li>\n{item.name}\n <button type='button'>Delete</button></li>".encode('utf-8') for item in classList))
        html = html.replace(b"<!-- ITEMS -->", make_html_list().encode('utf-8'))
        self.wfile.write(html)
        
    def do_POST(self):
        # Parse the form data posted
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))
        action = data.get("action", [""])[0]
        print(action)
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

