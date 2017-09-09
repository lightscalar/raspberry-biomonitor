from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from eventlet import wsgi
import eventlet

# Hidden imports (required for compiling via pyinstaller)
import dns
import dns.e164
import dns.namedict
import dns.tsigkeyring
import dns.update
import dns.version
import dns.zone

'''RESTFUL API for the Biomonitor.'''
app = Flask(__name__)
CORS(app)

@app.route('/')
def get():
    return 'Welcome to my server!'


if __name__ == '__main__':
    wsgi.server(eventlet.listen(('localhost', 8080)), app)
