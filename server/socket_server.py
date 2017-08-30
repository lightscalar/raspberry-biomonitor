'''WEB SOCKET Data Server

To launch this service, run:

    gunicorn --worker-class eventlet -w 1 socket_server:app

'''
from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, send, emit
from pymongo import MongoClient
from device import BioBoard

app = Flask(__name__)
socketio = SocketIO(app)
connection_status = False
client = MongoClient()
db = client['biomonitor']

# Boot up an instance of the biomonitor.
board = BioBoard()
board.start()

# ------------------------------------------------
# SOCKET API:
# ------------------------------------------------
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


@socketio.on('start_record')
def start_record():
    print('Starting data collection.')


@socketio.on('stop_record')
def stop_record():
    '''Start recording data.'''
    print('Stopping data collection.')


def status_update(status):
    '''Send out a status update.'''
    socketio.emit('status', status)


@socketio.on('request_status')
def handle_message():
    '''Send out an updated system status.'''
    emit('status', board._status)


# Add event handlers to the board.
board.events.status_update = status_update

