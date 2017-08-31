from collections import deque
from events import Events
from ipdb import set_trace as debug
from queue import Queue
import threading
from time import sleep, time

from arctic import Arctic
from filters import *


class Stream(object):
    '''Provides a thread for writing data chunks to a database or socket API.
       Pass into the BioBoard as a streamable object. Can be configured
       to handle realtime filtering of data chunks, and so on.
    '''

    def __init__(self, socket=None):
        '''Create a new stream object.'''

        # Set up the event bus.
        self.events = Events()
        self.do_process_data = False

        # Set up the data filters.
        self.data = None
        self.channel_number = None
        self.freq_cutoff = 10
        self.filter_order = 5
        self.filter_coefs = {0:[], 1:[], 2:[], 3:[], 4:[]}

        # Socket communications.
        self.socket = socket

        # Set up the connection to Arctic.
        self.store = Arctic('localhost')
        self.session_id = None
        self.library = None
        self.field_names = \
                ['board_time', 'sys_time', 'values',\
                 'filtered_values', 'filter_coefs']

        # Define the queue to hold data processing jobs.
        self.q = Queue()

        # Define the workers.
        nb_workers = 2
        target = self.process_data
        for _ in range(nb_workers):
            worker = threading.Thread(target=target, args=(self.q,),\
                    daemon=True)
            worker.start()

    def process_data(self, q):
        '''Processor for the data queue.'''
            # If data is present, process it and broadcast to outlets.

        while True:
            # Grab the data and reformat for processing/saving.
            channel_number, raw_data = q.get()
            data = {}
            data['channel_number'] = channel_number
            data['board_time'] = np.array([d[0] for d in raw_data])
            data['sys_time'] = np.array([d[1] for d in raw_data])
            data['values'] = np.array([d[2] for d in raw_data])

            # Run lowpass filter over the data.
            data = self.filter_data(data)

            # Push data through socket, if available.
            self.broadcast_data(data)

            # Save data to database.
            self.save_to_database(data)

            # Processing is done
            q.task_done()

    def filter_data(self, data):
        '''Filter the data.'''
        channel_number = data['channel_number']
        coefs = self.filter_coefs[channel_number]
        y_filt, coefs = lowpass(data['board_time'], data['values'],\
                self.filter_order, self.freq_cutoff, coefs)
        self.filter_coefs[channel_number] = coefs
        data['filtered_values'] = y_filt
        data['filter_coefs'] = coefs
        return data

    def save_to_database(self, data):
        '''Save data to the current database.'''
        if self.session_id is not None:
            channel_number = data['channel_number']
            for field_name in self.field_names:
                key = '{:02d}-{:s}'.format(channel_number, field_name)
                value = data[field_name]
                self.library.append(key, value)
            print('Data Saved')

    def broadcast_data(self, data):
        '''Broadcast current data on the socket.'''
        if self.socket is not None:
            self.socket.emit('data_package', self.data)

    def set_session_id(self, session_id):
        '''Set the current session ID.'''
        self.session_id = str(session_id)
        if session_id not in self.store.list_libraries():
            self.store.initialize_library(session_id)
        self.library = self.store[session_id]

    def push(self, channel_number, data):
        '''Enqueue the current data package.'''
        if len(data) > 0:
            self.q.put((channel_number, data))


if __name__ == '__main__':

    from pylab import *
    ion()
    close('all')

    # Make some data to play with.
    v = Vessel('good_collection.dat')
    t = v.t * 1e-6
    y = v.y

    # Simulate some data filtering.
    s = Stream()
    s.set_session_id('test-session-09')
    # s.start()

    # data = [(d[0], d[0], d[1]) for d in zip(t, y)]
    # s.push(1,data)

    for itr in range(0, len(t),1000):
        t_ = t[itr:itr+1000]
        y_ = y[itr:itr+1000]
        data = [(d[0], d[0], d[1]) for d in zip(t_, y_)]
        s.push(0, data)
        sleep(0.01)

    # s.kill()
    # y_filt = s.library.read('01-filtered_values').data
    # t_db = s.library.read('01-board_time').data
    # close('all')

    # plot(y_filt)

