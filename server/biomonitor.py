from flask_socketio import SocketIO, send, emit
from flask import Flask
from glob import glob
import numpy as np
from queue import Queue
import re
import serial
import threading
from time import time, sleep
from scipy.signal import butter, lfilter
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

    def __init__(self, sampling_rate=50, freq_cutoff=10):
        '''See if we can find a valid biomonitor device'''
        threading.Thread.__init__(self)
        self.port = None
        self.go = True

        # Set up the filters.
        filter_order = 5
        self.sampling_rate = sampling_rate
        self.dt = 1/sampling_rate
        nyquist = 0.5 * sampling_rate
        f_low = freq_cutoff/nyquist
        self.a, self.b  = butter(filter_order, f_low, 'low', analog=False)

        # Channel specific stats.
        self.allowed_channels = [0]
        self.stats = {}
        for chn in self.allowed_channels:
            self.stats[chn] = {'zi': np.zeros(filter_order), 'last_send': 0}

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
                print('Cannot connect to port {}.'.format(self.client.port))
                print('Trying again.')
                sleep(0.2)
            else:
                print('Connected to port {}.'.format(self.client.port))

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
            else:
                print('Connected to board.')

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

    def filter(self, channel, value):
        '''Filter the current value.'''
        zi = self.stats[channel]['zi']
        y, zf = lfilter(self.a, self.b, [value], zi=zi)
        self.stats[channel]['zi'] = zf
        return y[0]

    def read_data(self, ser):
        '''Read data, filter data, transmit data across socket.'''
        line = ser.readline()
        chn, timestamp, value = self.parse_biomonitor(line)
        if chn in self.allowed_channels:
            if (time() - self.stats[chn]['last_send']) >= self.dt:
                self.stats[chn]['last_send'] = time()
                filt_val = self.filter(chn, value)
                obj = json.dumps([chn, time(), timestamp, value, filt_val])
                self.client.send_json(obj)

    def run(self):
        '''Collect data and send it to a socket connection.'''
        with serial.Serial(self.port, BAUD_RATE) as ser:
            while self.go:
                self.read_data(ser)

    def stop(self):
        self.client.close()
        self.go = False

if __name__ == '__main__':

    bio = Biomonitor()

