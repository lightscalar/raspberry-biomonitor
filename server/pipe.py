from arctic import Arctic
from events import Events
from queue import Queue
import threading
from time import sleep, time
from filters import *



class Pipe(object):
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
        self.target_sampling_rate = 100

        # Socket communications.
        self.socket = socket

        # Set up the connection to Arctic.
        self.store = Arctic('localhost')
        self.session_id = None
        self.library = None
        self.field_names = \
                ['bio_time', 'sys_time', 'values',\
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
        '''Process data in the queue.'''
        # If data is present, process it and broadcast to outlets.
        while True:
            # Grab the data and reformat for processing/saving.
            channel_number, raw_data = q.get()
            data = {}
            data['channel_number'] = channel_number
            data['bio_time'] = np.array([d[0] for d in raw_data])
            data['sys_time'] = np.array([d[1] for d in raw_data])
            data['values'] = np.array([d[2] for d in raw_data])

            # Run lowpass filter over the data.
            data = self.filter_data(data)

            # Downsample data for socket connection.
            data = self.downsample_data(data)

            # Push data through socket, if available.
            self.broadcast_data(data)

            # Save data to database.
            self.save_to_database(data)

            # Processing is done
            q.task_done()

    def downsample_data(self, data):
        '''Downsample data to target sampling rate.'''
        tsr = self.target_sampling_rate
        t_, v_= downsample(data['bio_time'], data['filtered_values'], tsr)
        data['full_sampling_rate'] = 1 / np.median(np.diff(data['bio_time']))
        data['sampling_rate'] = self.target_sampling_rate
        data['downsampled_bio_time'] = t_
        data['downsampled_filtered_values'] = v_
        return data

    def filter_data(self, data):
        '''Filter the data.'''
        channel_number = data['channel_number']
        coefs = self.filter_coefs[channel_number]
        y_filt, coefs = lowpass(data['bio_time'], data['values'],\
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
            package = {}
            package['time'] = data['downsampled_bio_time']
            package['vals'] = data['downsampled_filtered_values']
            package['channel_number'] = data['downsampled_bio_time']
            package['sampling_rate'] = data['full_sampling_rate']
            self.socket.emit('data_package', package)

    def set_session_id(self, session_id):
        '''Set the current session ID.'''
        self.session_id = str(session_id)
        if session_id not in self.store.list_libraries():
            self.store.initialize_library(session_id)
        self.library = self.store[session_id]

    def push(self, channel_number, data):
        '''Enqueue the current data package.'''
        print('PUSHING DATA.')
        if len(data) > 0:
            self.q.put((channel_number, data))


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

