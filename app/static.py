import eventlet
eventlet.monkey_patch()
import http.server
import socketserver
import os

# Serve static index.html file from the /site directory.
PORT = 5000

if __name__ == '__main__':
    web_dir = os.path.join(os.path.dirname(__file__), '../dist')
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()
