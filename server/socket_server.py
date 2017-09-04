from antenna import Antenna
from comm_link import *
from flask import Flask
from flask_socketio import SocketIO, send, emit
import signal
import sys
from utils import Vessel


'''WEB SOCKET Data Server
---
To launch this service, run:

    gunicorn --worker-class eventlet -w 1 socket_server:app
'''

# Define the application.
app = Flask(__name__)
socketio = SocketIO(app)
connection_status = False

# Define communication objects.
data_stream = Server()
antenna = Antenna(socketio)

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
    v = Vessel('db.cmd')
    v.command = 'start_record'
    v.session_id = session_id
    v.save()


@socketio.on('stop_record')
def stop_record():
    '''Start recording data.'''
    print('Stopping data collection.')
    emit('status', {'connected': True, 'message': 'Data Available'})
    v = Vessel('db.cmd')
    v.command = 'stop_record'
    v.save()


# ------------------------------------------------
# CALLBACK FUNCTIONS.
# ------------------------------------------------
def status_update(status):
    '''Send out a status update.'''
    socketio.emit('status', status)


# Set up an event handler to broadcast and write data.
# data_connection.events.on_data_received += broadcast_data
data_stream.events.on_data += antenna.push


