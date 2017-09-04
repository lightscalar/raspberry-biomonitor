from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, send, emit
from pymongo import MongoClient
import signal
import sys
from comm_link import Server
from pipe import *
from mathtools.utils import Vessel


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

connection_status = False
datastore = Vessel('test.dat')
datastore.data = []

# Listen for a kill signal. Close down biomonitor connection.
def exit_gracefully(signal, frame):
    '''When we kill the server (via CTL-C), gracefully close board
       connections as well.
    '''
    status = {'message': 'System Crashed | Restart Required'}
    status['connected'] = False
    print('Handling Final communications')
    socketio.emit('status', status)
    sys.exit(0)

signal.signal(signal.SIGINT, exit_gracefully)

# ------------------------------------------------
# SOCKET API:
# ------------------------------------------------
@socketio.on('connect')
def connected():
    '''Set system connection status.'''
    connection_status = True
    emit('status', {'connected': True, 'message': 'Data Available'})


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
def start_record(session_id):
    print('Starting data collection to {:s}'.format(session_id))
    emit('status', {'connected': True, 'message': 'Recording Data'})
    pipe.start_recording(session_id)


@socketio.on('stop_record')
def stop_record():
    '''Start recording data.'''
    print('Stopping data collection.')
    emit('status', {'connected': True, 'message': 'Data Available'})
    pipe.stop_recording()


# ------------------------------------------------
# CALLBACK FUNCTIONS.
# ------------------------------------------------
def status_update(status):
    '''Send out a status update.'''
    socketio.emit('status', status)


def broadcast_data(data):
    '''Broadcast data to UI.'''
    # datastore.data.append(data)
    socketio.emit('data_package', data)
    # if var_iter==1000:
    #     datastore.save()
    #     var_iter = 0


# Set up an event handler to broadcast and write data.
data_connection.events.on_data_received += broadcast_data
# data_connection.events.on_data_received += pipe.push


