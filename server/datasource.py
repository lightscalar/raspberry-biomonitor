from flask_socketio import SocketIO, send, emit
from flask import Flask
from glob import glob
import numpy as np
from queue import Queue
import re
import serial
from threading import Thread
from time import time, sleep
from scipy.signal import butter, lfilter
from comm_link import Client
from mathtools.utils import Vessel


# Define parameters.
BAUD_RATE = 9600
BIOMONITOR_REGEX = r"(B1)\s*(\d*)\s*(\w{0,8})\s*(\w*)"
MAXVAL = 2**24-1
MAXREF = 2.5
COVFAC = MAXREF*(1/MAXVAL)


def find_serial_devices():
    '''Find serial devices connected to the computer.'''
    SERIAL_REGEX = r"/dev/tty.usbmodem"
    devices = glob('/dev/*')
    valid_devices = []
    for device in devices:
        if re.search(SERIAL_REGEX, device):
            valid_devices.append(device)
    return valid_devices


class DataSource(Thread):
    '''Connect to biomonitor device and push data to a socket connection.'''

    def __init__(self):
        '''See if we can find a valid biomonitor device'''
        Thread.__init__(self)
        self.port = None
        self.go = True

        self.allowed_channels = [0]

        # Connect to the hardware.
        self.connect_to_board()

        # Connect to the buffer file.
        self.buffer = {}
        for chn in self.allowed_channels:
            self.buffer[chn] = Vessel('buffer-{:02d}.dat'.format(chn))
        self.clear_buffer()
        self.chunk_size = 2000

        # Define the workers.
        self.q = Queue()
        nb_workers = 10
        target = self.save_data
        for _ in range(nb_workers):
            worker = Thread(target=target, args=(self.q,), daemon=True)
            worker.start()

        # Start local.
        self.start()

    def clear_buffer(self):
        '''Clear the current data buffer.'''
        for chn in self.allowed_channels:
            self.buffer[chn].counter = 0
            self.buffer[chn].t = []
            self.buffer[chn].t_sys = []
            self.buffer[chn].v = []

    def save_data(self, q):
        '''Save data to the disk.'''
        while True:
            data = q.get()
            chn = data[0]
            self.buffer[chn].t.append(data[1])
            self.buffer[chn].v.append(data[2])
            self.buffer[chn].t_sys.append(data[3])
            self.buffer[chn].counter += 1
            if self.buffer[chn].counter > self.chunk_size:
                self.buffer[chn].save()
            q.task_done()

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

    def read_data(self, ser):
        '''Read data, filter data, transmit data across socket.'''
        line = ser.readline()
        chn, timestamp, value = self.parse_biomonitor(line)
        if chn in self.allowed_channels:
            # self.data[chn].append([chn, timestamp, value])
            self.q.put([chn, timestamp, value, time()])

    def run(self):
        '''Collect data and send it to a socket connection.'''
        with serial.Serial(self.port, BAUD_RATE) as ser:
            while self.go:
                self.read_data(ser)

    def stop(self):
        self.go = False

if __name__ == '__main__':

    fountain = DataSource()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        fountain.stop()


