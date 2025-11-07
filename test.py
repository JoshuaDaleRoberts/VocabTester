import http.server
import socketserver
import pickle
import os
import cgi
import textract
from urllib.parse import urlparse, parse_qs
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

#Initialize directory for document uploads
os.makedirs("uploads", exist_ok=True)

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
            # Serve class page
            with open("class.html", "rb") as f:
                html = f.read()
            class_number = page.query
            class_name = classList[int(class_number)].name
            # Handles title of class page
            html = html.replace(b"<!-- c -->", class_name.encode('utf-8'))
            # Handles form building for uploads
            html = html.replace(b"replace_with_class_name", class_name.encode('utf-8'))
            # grabbing uploaded files
            try:
                file_array = os.listdir(f"uploads{os.sep}class_{class_name}")
                print(file_array)
            except FileNotFoundError:
                file_array = []
            file_list_html = ""
            for file in file_array:
                file_list_html += f'<li><a href="/uploads/class_{class_name}/{file}" download="{file}">{file}</a></li>'
            html = html.replace(b"<!-- FILES -->", file_list_html.encode('utf-8'))
            
        else:
            # Serve main page
            with open("index.html", "rb") as f:
                html = f.read()
            html = html.replace(b"<!-- ITEMS -->", make_html_list().encode('utf-8'))
            
        self.wfile.write(html)
        
    def do_POST(self):
        # Parse the form data posted
        content_length = int(self.headers['Content-Length'])
        content_type = self.headers.get('Content-Type')
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': content_type}
        )
        action = form.getvalue("action")
        print("POSTING")

        # Add Vocab
        if action == "add":
            vocab_value = form.getvalue("vocab")
            a = Vocab(vocab_value)
            classList.append(a)
            write_to_file()

        # Delete Vocab
        if action == "delete":
            id_value = int(form.getvalue("id", [-1])[0])
            classList.pop(id_value)
            write_to_file()
        
        # Storing and parsing file uploads
        if action == "upload":
            #write file to uploads directory within the class specified
            class_name = form.getvalue("class_name")
            os.makedirs(f"uploads{os.sep}class_{class_name}", exist_ok=True)
            file_data = form['file']
            if file_data.filename:
                with open(f"uploads{os.sep}class_{class_name}{os.sep}{file_data.filename}", "wb") as f:
                    f.write(file_data.file.read())

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

