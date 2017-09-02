import threading
from collections import deque
import time
from events import Events
import logging
import numpy as np
import serial
from serial_lib import *
import re


class BioBoard(threading.Thread):
    '''Provides a direct connection to the biomonitor Serial port.
    -----
        Connect to a biomonitor device on a separate thread. Once started, an
        instance will search for a valid biomonitor device. When connected, it
        read data from the serial port. If a stream is started, and a suitable
        stream object is provided, data will stream to that object (could be an
        in-memory array, a Mongo database, etc.).

        Pains have been taken to ensure the connection fails gracefully, but
        YMMV.
    '''

    # def __init__(self, port=None, baud_rate=921600, verbose=logging.INFO):
    def __init__(self, port=None, baud_rate=9600, verbose=logging.INFO):
        '''Create a new thread that will communicate with the biomonitor.
        INPUTS
            port - string
                Name of port to connect to. If no port is specified we'll look
                for available USB ports and check them.
            baud_rate - int
                The serial port's expected baud rate.
            verbose - int
                Set the logging level of the connection. Default is INFO.
        '''
        # We'll run in a separate thread.
        threading.Thread.__init__(self)

        # Set up the event bus.
        self.events = Events()

        # Connect to the device.
        logging.basicConfig(level=verbose)
        self.log = logging.getLogger(__name__)
        self.info = self.log.info

        # Some variables for handling bad connection detection.
        self._bad_data_count = 0
        self._last_read_bad = False

        # Internal data buffer.
        self.pipe = None
        self.AVAILABLE_CHANNELS = [0, 1, 2, 3]
        self.BUFFER_SIZE = 5
        self.buffer = {}
        self.buffer_counts = {}
        for channel in self.AVAILABLE_CHANNELS:
            self.buffer[channel] = deque([], self.BUFFER_SIZE)
            self.buffer_counts[channel] = 0

        # Status variables.
        self._is_connected = False
        self.go = True
        self.do_stream = False
        self._trouble = False
        self._behaving = False

        # Connection variables.
        self.port = port
        self.baud_rate = baud_rate

        # Board communications & conversion stuff.
        self.COV_FACTOR = 2.5 / (2**24-1)
        self.bio_regex = r"(B1)\s*(\d*)\s*(\w{0,8})\s*(\w*)"

    def _set_status(self, message=''):
        '''Set the system status and broadcase update to subscribers.'''
        self._status = {}
        self._status['connected'] = self._is_connected
        self._status['streaming'] = self.do_stream
        self._status['behaving'] = self._behaving
        self._status['message'] = message
        self.events.status_update(self._status)
        self.info(message)

    def run(self):
        '''This is the main loop of the thread.'''
        self._set_status('Looking for Biomonitor')
        while self.go: # main loop
            try:
                # Attempt to connect to the biomonitor!
                while (not self.is_connected) and (self.go):
                    self.connect()

                # We're connected, so open that serial port up!
                with serial.Serial(self.port, self.baud_rate, timeout=2) as\
                        ser:
                    # if (self.is_connected and self.go):
                    #     self._set_status('Data Available')
                    while (self.is_connected and self.go):
                        self.collect(ser)

                # And we're leaving main run loop & the thread, honorably.
                self._set_status('Closing BioDriver. Bye!')
            except:
                # Something went sideways.
                message = 'Biomonitor Error | Attempting Reconnect'
                self._is_connected = False
                self.log.exception(message)
                self._set_status(message)

    def kill(self):
        '''Kill this thread, with moderate prejudice.'''
        self.go = False
        self._is_connected = False

    def connect(self):
        '''Attempt to connect to the serial monitor.'''
        ports = find_serial_devices()
        if len(ports) == 0:
            self._set_status('Looking for Biomonitor')
        for port in ports:
            self._set_status('Pinging {:s}'.format(port))
            if self.ping(port):
                message = 'Connected to Biomonitor @{:s}'.format(port)
                self._set_status(message)
                self.port = port
                self._is_connected = True
                return # leave this search; we've found our man.

    def ping(self, port):
        '''Ping the serial port. See if a legit biomonitor lives there.'''
        with serial.Serial(port, self.baud_rate, timeout=1) as ser:
            try:
                output = ser.readline()
            except:
                message = 'Serial connection failed unexpectedly'
                self.events.status_update(message)
                output = ''
            parsed = re.search(self.bio_regex, str(output))
            return ((parsed) and (parsed.group(1) == 'B1')) # really legit?

    def collect(self, ser):
        '''Collect data from current serial connection.'''

        # Read the data coming from the serial channel.
        channel, board_timestamp, value = read_data(ser)

        # Buffer the data, if there is any.
        if channel is not None and self.do_stream:
            sys_timestamp = board_timestamp
            converted_value = value * self.COV_FACTOR
            data = (board_timestamp*1e-6, sys_timestamp, converted_value)
            self.buffer[channel].append(data)
            self.buffer_counts[channel] += 1

            # If we've accumulated a chunk, let's push it out.
            if self.buffer_counts[channel] == self.BUFFER_SIZE:
                self.buffer_counts[channel] = 0
                if self.pipe:
                    self.pipe.push(channel, self.buffer[channel])

        # If no valid channel is present, increment bad_data_count.
        if (channel is None):
            self._behaving = False
            self._set_status('Data Unavailable')
            self._trouble = True
            if self._last_read_bad:
                self._bad_data_count += 1
            self._last_read_bad = True

            # If we have two consecutive errors, try to reconnect.
            if self._bad_data_count > 1:
                self._is_connected = False
                self._trouble = False
        else:
            self._last_read_bad = False
            self._bad_data_count = 0
            self._trouble = False
            if not self._behaving:
                self._behaving = True
                self._set_status('Data Available')

    def pipe_to(self, pipe):
        '''Start saving data to specified filename via a time series object.'''
        self.pipe = pipe

    def start_stream(self):
        '''Start streaming data to the database/socket.'''
        if self.pipe is not None:
            self.do_stream = True
            self._set_status('Recording Data')
        else:
            self._set_status('Streaming Unavailable | Add Stream Connection')

    def stop_stream(self):
        ''' Turn stream to database/socket off.'''
        if self.do_stream:
            self.do_stream = False
            self._set_status('Data Available')
        else:
            self._set_status('Cannot Stop Stream | Not Currently Streaming')

    @property
    def status_message(self):
        if self.do_stream:
            message = 'Streaming Data'
        elif self.is_connected:
            message = 'Biomonitor Connected'
        elif self._trouble:
            message = 'Data Unavailable'
        else:
            message = 'Searching for Biomonitor'
        return message

    @property
    def is_active(self):
        '''Return Boolean indicating whether the thread is alive.'''
        return self.isAlive()

    @property
    def is_connected(self):
        '''Returns Boolean indicating whether we're talking to the board.'''
        return self._is_connected


if __name__ == '__main__':

    # Open a connection to the board. Try to start reading some data.
    board = BioBoard()
    board.start()

    if True:
        from pipe import *
        pipe = Pipe()


