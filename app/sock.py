from antenna_x import Antenna
from engine import Engine
from flask import Flask
from flask_socketio import SocketIO, send, emit
from prepare_downloads import *
import signal
import sys


'''WEB SOCKET Data Server'''

# Define the application.
PORT = 5200
app = Flask(__name__)
socketio = SocketIO(app)
connection_status = False
engine = Engine()


# ------------------------------------------------
# SOCKET API:
# ------------------------------------------------
@socketio.on('connect')
def connected():
    '''Set system connection status.'''
    connection_status = True
    print('Connected to client.')
    emit('status', {'connected': True, 'message': 'Data Available'})


@socketio.on('set_session')
def set_session(session_id):
    '''Set the proper session ID in the stream object.'''
    engine.start_recording(session_id)


@socketio.on('disconnect')
def disconnected():
    '''System is disconnected.'''
    connection_status = False
    print('Disconnected from client')


@socketio.on('downloadData')
def prepare_data(session_id):
    '''System is disconnected.'''
    print('Preparing data for session {}'.format(session_id))
    file_location = create_csv(session_id)
    socketio.emit('dataReady', file_location)


@socketio.on('start_record')
def start_record(session_id):
    print('Starting data collection to {:s}'.format(session_id))
    engine.start_recording(session_id)
    message = 'Recording Data'
    status = {'isRecording': engine.is_recording, 'message': message,\
            'connected': True}
    emit('status', status)


@socketio.on('stop_record')
def stop_record():
    '''Start recording data.'''
    print('Stopping data collection.')
    engine.stop_recording()
    message = 'Data Available'
    status = {'isRecording': engine.is_recording, 'message': message,\
            'connected': True}
    emit('status', status)

@socketio.on('requestStatus')
def send_status():
    if engine.is_recording:
        message = 'Recording Data'
    else:
        message = 'Data Available'
    status = {'isRecording': engine.is_recording, 'message': message,\
            'connected': True}
    print(status)
    emit('status', status)


# ------------------------------------------------
# CALLBACK FUNCTIONS.
# ------------------------------------------------
def status_update(status):
    '''Send out a status update.'''
    socketio.emit('status', status)


if __name__ == '__main__':

    # Antenna broadcasts data to the UI.
    antenna = Antenna(socketio)

    # Define communication objects.
    engine.events.on_data += antenna.push

    # Launch server. Will use eventlet, if available.
    socketio.run(app, port=PORT, debug=False)
