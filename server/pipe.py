from arctic import Arctic
from events import Events
import json
from queue import Queue
import threading
from time import sleep, time
from filters import *


class Pipe(object):
    '''Provides a thread for writing data chunks to an arctic database.'''

    def __init__(self, socket=None):
        '''Create a new stream object.'''

        # Set up the event bus.
        self.events = Events()
        self.recording = False

        # Set up the data filters.
        self.data = None
        self.allowed_channels  = [0]

        # Set up the connection to Arctic.
        self.store = Arctic('localhost')
        self.session_id = None
        self.library = None
        self.field_names = ['sys_time', 'bio_time', 'values', 'filt_values']

        # Define the queue to hold data processing jobs.
        self.q = Queue()

        # Define the workers.
        nb_workers = 10
        target = self.process_data
        for _ in range(nb_workers):
            worker = threading.Thread(target=target, args=(self.q,),\
                    daemon=True)
            worker.start()

    def process_data(self, q):
        '''Process data in the queue.'''
        # If data is present, process it and broadcast to outlets.
        while True:
            data = json.loads(q.get())
            self.write_data(data)
            q.task_done()

    def write_data(self, data):
        '''Write data to the arctic data store.'''
        if not self.recording:
            return
        channel_number = data[0]
        data = data[1:]
        for itr, field_name in enumerate(self.field_names):
            key = '{:02d}-{:s}'.format(channel_number, field_name)
            value = np.array([data[itr]])
            self.library.append(key, value)

    def start_recording(self, session_id):
        '''Start streaming data to the Arctic datastore.'''
        self.session_id = str(session_id)
        if session_id not in self.store.list_libraries():
            self.store.initialize_library(session_id)
        self.library = self.store[session_id]
        self.recording = True

    def stop_recording(self):
        '''Stop writing to the database.'''
        self.recording = False
        self.session_id = None

    def push(self, data):
        '''Enqueue the current data package.'''
        if len(data) > 0:
            self.q.put(data)
