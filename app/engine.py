import numpy as np
from events import Events
from sockets import Server
from datastore import *
from ipdb import set_trace as debug
from filters import *


class Engine(object):

    def __init__(self):
        '''Set up socket connections/event bus.'''
        self.server = Server()
        self.events = Events()

        # Boot up datastore/etc.
        self.valid_keys = ['t', 't_sys', 'val', 'filtered']
        self.datastore = DataStore()
        self.session_id = '2017.09.07.b'
        self.is_recording = True
        self.is_broadcasting = True

        # Configure filters.
        self.allowed_channels = [0, 1, 2]
        self.freq_cutoff = 10
        self.filter_order = 5
        self.downsample_rate = 50
        self.zi = {}
        for chn in self.allowed_channels:
            self.zi[chn] = np.zeros(self.filter_order)

        # Listen for data from the server.
        self.server.events.on_data += self.data_received

    def data_received(self, data):
        '''Data has been received by the server.'''
        print(data)
        # Broadcast data to socket connections.
        # self.events.on_data(data)

        # If we have a session id, save the data.
        for channel in data.keys():
            ichn = int(channel)
            d = data[channel]
            d['filtered'], self.zi[ichn] = \
                lowpass(d['t'], d['val'], freq_cutoff=self.freq_cutoff,\
                filter_order=self.filter_order, zi=self.zi[ichn])

            # Broadcast the data.
            if self.is_broadcasting:
                downsampled = downsample(d['t'], d['filtered'],\
                        self.downsample_rate)
                package = [ichn, downsampled]
                self.events.on_data(package)

            # Save the data.
            if self.is_recording:
                for key, val in d.items():
                    if key in self.valid_keys:
                        self.datastore.write(self.session_id, ichn, key,\
                                np.array(val))


    def start_recording(self, session_id):
        '''Start saving data to datastore.'''
        self.session_id = session_id
        self.is_recording = True

    def stop_recording(self):
        '''Stop streaming to the datastore.'''
        self.session_id = None
        seldf.is_recording = False

    def kill(self):
        '''Close the socket connection.'''
        self.server.close()


if __name__ == '__main__':
    e = Engine()

