import eventlet
from eventlet import wsgi
eventlet.monkey_patch()
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

PORT = 5000
app = Flask(__name__, static_folder='../dist/static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('../dist', 'index.html')

if __name__ == '__main__':
    # Run the webserver.
    app.run()
