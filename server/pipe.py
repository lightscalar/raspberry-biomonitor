from arctic import Arctic
from events import Events
from queue import Queue
import threading
from time import sleep, time
from filters import *


class Pipe(object):
    '''Provides a thread for writing data chunks to an arctic database.
       Pass into the BioBoard as a streamable object. Can be configured
       to handle realtime filtering of data chunks, and so on.
    '''

    def __init__(self, socket=None):
        '''Create a new stream object.'''

        # Set up the event bus.
        self.events = Events()
        self.do_write_data = False

        # Set up the data filters.
        self.data = None
        self.allowed_channels  = [0]

        # Set up the connection to Arctic.
        self.store = Arctic('localhost')
        self.session_id = None
        self.library = None
        self.field_names = ['sys_time', 'bio_time', 'values', 'filtered_values']

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
            if self.recording and (self.session_id is not None):
                data = json.loads(q.get())
                self.write_data(self, data)
                q.task_done()
            else:
                q.task_done()

    def write_data(self, data):
        '''Write data to the arctic data store.'''
        channel = data[0]
        data = data[1:]
        for itr, field_name in enumerate(self.field_names):
            key = '{:02d}-{:s}'.format(channel_number, field_name)
            value = data[itr]
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


    def set_session_id(self, session_id):
        '''Set the current session ID.'''
        self.session_id = str(session_id)
        if session_id not in self.store.list_libraries():
            self.store.initialize_library(session_id)
        self.library = self.store[session_id]

    def push(self, channel_number, data):
        '''Enqueue the current data package.'''
        if len(data) > 0:
            self.q.put((data)

    def put(self, channel_number, raw_data):
        '''Non-thread based version.'''
        data = {}
        data['start'] = time()
        data['channel_number'] = channel_number
        data['bio_time'] = np.array([d[0] for d in raw_data])
        data['sys_time'] = np.array([d[1] for d in raw_data])
        data['values'] = np.array([d[2] for d in raw_data])
        data = self.filter_data(data)
        data = self.downsample_data(data)
        self.broadcast_data(data)


# if __name__ == '__main__':

#     from pylab import *
#     ion()
#     close('all')

#     # Make some data to play with.
#     v = Vessel('good_collection.dat')
#     t = v.t * 1e-6
#     y = v.y

#     # Simulate some data filtering.
#     s = Stream()
#     s.set_session_id('test-session-09')
#     # s.start()

#     # data = [(d[0], d[0], d[1]) for d in zip(t, y)]
#     # s.push(1,data)

#     for itr in range(0, len(t),1000):
#         t_ = t[itr:itr+1000]
#         y_ = y[itr:itr+1000]
#         data = [(d[0], d[0], d[1]) for d in zip(t_, y_)]
#         s.push(0, data)
#         sleep(0.01)

