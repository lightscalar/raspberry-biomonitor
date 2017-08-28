'''WEB SOCKET Data Server

To launch this service, run:

    gunicorn --worker-class eventlet -w 1 socket_server:app

'''
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from pymongo import MongoClient()

app = Flask(__name__)
socketio = SocketIO(app)
connection_status = False
client = MongoClient()
db = client['biomonitor']

@socketio.on('connect')
def connected():
    '''Set system connection status.'''
    connection_status = True
    print('> Connected')

@socketio.on('disconnect')
def disconnected():
    '''System is disconnected.'''
    connection_status = False
    print('> Disconnected')

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    emit('ack', {'name': 'Hugo James'})

@socketio.on('status_request')
def status_request(json):
    pass

@socketio.on('message')
def handle_message(message, data):
    print('received message: ' + message)
    print(data)

