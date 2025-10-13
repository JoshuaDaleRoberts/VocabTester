import http.server
import socketserver

port = 2704
Handler = http.server.SimpleHTTPRequestHandler

from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <body>
            <form method="POST">
                <button type="submit">Hello World</button>
            </form>
        </body>
        </html>
        """)

    def do_POST(self):
        print("hello world")  # This prints to the console
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <body>
            <form method="POST">
                <button type="submit">Hello World</button>
            </form>
        </body>
        </html>
        """)
if __name__ == "__main__":
    server = HTTPServer(('localhost', 8000), SimpleHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()



