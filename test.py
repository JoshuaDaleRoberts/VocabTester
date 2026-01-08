import http.server
import socketserver
import pickle
import os
import cgi
import pypdf
from urllib.parse import urlparse, parse_qs, quote, unquote
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

    # Handle Get requests, different pages
    def do_GET(self):
        
        page = urlparse(self.path)

        # Serve class page
        if page.path == "/class":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Access class.html filee
            with open("class.html", "rb") as f:
                html = f.read()

            # Sets values for html replacements
            class_number = page.query
            class_name = classList[int(class_number)].name

            # Handles title of class page
            html = html.replace(b"<!-- c -->", class_name.encode('utf-8'))

            # Handles form building for uploads
            html = html.replace(b"replace_with_class_name", class_name.encode('utf-8'))

            # Grabs uploaded files
            try:
                file_array = os.listdir(f"uploads{os.sep}class_{class_name}")
            except FileNotFoundError:
                file_array = []
            file_list_html = ""

            # Makes <li> of uploaded files
            for file in file_array:
                safe = quote(file)
                file_list_html += (f'<li><a href="/download?class={class_name}&file={safe}">{file}</a></li>')

            # And inserts the <li>s onto the page
            html = html.replace(b"<!-- FILES -->", file_list_html.encode('utf-8'))
            self.wfile.write(html)


        elif page.path == "/download":

            # Handle file download requests
            params = parse_qs(page.query)

            class_name = params.get("class", [None])[0]
            filename = params.get("file", [None])[0]
            filename = unquote(filename)

            # Basic validation
            if not class_name or not filename:
                self.send_error(400, "Bad request")
                return

            # Prevent path traversal
            if ".." in class_name or ".." in filename or "/" in filename:
                self.send_error(403, "Forbidden")
                return

            filepath = os.path.join("uploads", f"class_{class_name}", filename)
            print(f"filepath: {filepath}")

            if not os.path.isfile(filepath):
                self.send_error(404, "File not found")
                return

            # Serve file as download
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header(
                "Content-Disposition",
                f'attachment; filename="{filename}"'
            )
            self.send_header("Content-Length", os.path.getsize(filepath))
            self.end_headers()

            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
            return
        
        else:
            # Serve main page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
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
            text = pypdf.PdfReader(f"uploads{os.sep}class_{class_name}{os.sep}{file_data.filename}")
            print(text.pages[0].extract_text())


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

