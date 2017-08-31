from device import BioBoard
from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, send, emit
from pymongo import MongoClient
from pipe import *

'''WEB SOCKET Data Server
---
To launch this service, run:

    gunicorn --worker-class eventlet -w 1 socket_server:app

'''
# Define the application.
app = Flask(__name__)
socketio = SocketIO(app)

# Boot up an instance of the biomonitor.
board = BioBoard()
board.start()

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
    board.start_stream()


@socketio.on('stop_record')
def stop_record():
    '''Start recording data.'''
    print('Stopping data collection.')
    board.stop_stream()


def status_update(status):
    '''Send out a status update.'''
    socketio.emit('status', status)


@socketio.on('request_status')
def handle_message():
    '''Send out an updated system status.'''
    emit('status', board._status)


# Give the stream instance a socket.
pipe.socket = socketio

# Add event handlers to the board and add stream object.
board.events.status_update = status_update
board.pipe_to(pipe)
