import threading
from queue import Queue
import numpy as np
from glob import glob
import re
import serial
from time import time, sleep
from flask_socketio import SocketIO, send, emit
from flask import Flask
from comm_link import *


# Define parameters.
BAUD_RATE = 9600
BIOMONITOR_REGEX = r"(B1)\s*(\d*)\s*(\w{0,8})\s*(\w*)"
MAXVAL = 2**24-1
MAXREF = 2.5
COVFAC = MAXREF*(1/MAXVAL)

app = Flask(__name__)
socketio = SocketIO(app)


def find_serial_devices():
    '''Find serial devices connected to the computer.'''
    SERIAL_REGEX = r"/dev/tty.usbmodem"
    devices = glob('/dev/*')
    valid_devices = []
    for device in devices:
        if re.search(SERIAL_REGEX, device):
            valid_devices.append(device)
    return valid_devices


class Biomonitor(threading.Thread):
    '''Connect to biomonitor device and push data to a socket connection.'''

    def __init__(self):
        '''See if we can find a valid biomonitor device'''
        threading.Thread.__init__(self)
        self.port = None
        self.go = True

        # Connect to the hardware.
        self.connect_to_board()

        # Connect to the client.
        self.connect_to_server()

        # Start thread.
        self.start()

    def connect_to_server(self):
        '''Connect monitor to local web/socket server.'''
        connected = False
        while not connected:
            self.client = Client()
            connected = self.client.connected
            if not connected:
                print('Cannot connect to port {}'.format(self.client.port))
                print('Trying again.')
                sleep(0.2)

    def connect_to_board(self):
        '''Attempt to connect to the Biomonitor hardware.'''
        while self.port is None:
            valid_ports = find_serial_devices()
            for port in valid_ports:
                with serial.Serial(port, BAUD_RATE) as ser:
                    for _ in range(5):
                        raw_output = ser.readline()
                        scan = re.search(BIOMONITOR_REGEX, str(raw_output))
                        if scan is not None and scan.group(1) == 'B1':
                            self.port = port
                            break
            # Cannot find a good port?
            if self.port is None:
                print('Cannot find board.')
                print('Trying again.')
                sleep(0.2)

    def parse_biomonitor(self, line):
        '''Parse output from the Biomonitor.'''
        parse = re.search(BIOMONITOR_REGEX, str(line))
        (channel_number, timestamp, value) = None, None, None
        if parse:
            # We caught something!
            if parse.group(1) == 'B1':
                # Looks like we have some BioMonitor output.
                try: # channel number there?
                    channel_number = int(parse.group(2), 16)
                except:
                    pass
                try: # voltage value present?
                    value = int(parse.group(3),16) * COVFAC
                except:
                    pass
                try: # timestamp present?
                    timestamp = int(parse.group(4),16) * 1e-6 # to seconds
                except:
                    pass
        return (channel_number, timestamp, value)

    def run(self):
        '''Collect data and send it to a socket connection.'''
        last_send = time()
        stats = {}
        for chn in [0,1,2]:
            stats[chn] = {'n':0, 'mean':0, 'coefs': []}
        with serial.Serial(self.port, BAUD_RATE) as ser:
            while self.go:
                line = ser.readline()
                channel, timestamp, value = self.parse_biomonitor(line)
                if channel == 0:
                    if time() - last_send >= 0.02:
                        obj = json.dumps([channel, timestamp, value])
                        self.client.send_json(obj)
                        last_send = time()

    def stop(self):
        self.client.close()
        self.go = False

if __name__ == '__main__':

    bio = Biomonitor()

