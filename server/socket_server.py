from device import BioBoard
from biomonitor import *
from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, send, emit
from pymongo import MongoClient
from comm_link import Server
from pipe import *

'''WEB SOCKET Data Server
---
To launch this service, run:

    gunicorn --worker-class eventlet -w 1 socket_server:app
'''
# Get socket connection to Biomonitor source.
data_connection = Server()

# Define the application.
app = Flask(__name__)
socketio = SocketIO(app)

# Define the stream object.
pipe = Pipe()

# ------------------------------------------------
# SOCKET API:
# ------------------------------------------------
@socketio.on('connect')
def connected():
    '''Set system connection status.'''
    connection_status = True
    print('> Connected')


@socketio.on('set_session')
def set_session(session_id):
    '''Set the proper session ID in the stream object.'''
    stream.set_session(session_id)


@socketio.on('disconnect')
def disconnected():
    '''System is disconnected.'''
    connection_status = False
    print('> Disconnected')


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
    emit('status', {})

def broadcast_data(data):
    '''Broadcast data to UI.'''
    socketio.emit('data_package', data)


# Set up an event handler for data push.
data_connection.events.on_data_received = broadcast_data

# Give the stream instance a socket.
# pipe.socket = socketio

# Add event handlers to the board and add stream object.
# board.events.status_update = status_update
# board.pipe_to(pipe)
