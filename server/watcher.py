from arctic import Arctic
import sys
from events import Events
from ipdb import set_trace as debug
import json
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from comm_link import Client, Server
from filters import *
from utils import Vessel


class BufferProcessor(PatternMatchingEventHandler):
    '''Watches for changing data buffers. Filters contents and emits alert.'''

    patterns = ["*.dat", "*.cmd"]
    filter_order = 5

    def __init__(self, freq_cutoff=10):
        PatternMatchingEventHandler.__init__(self)

        # Define the event bus.
        self.client = Client()
        self.events = Events()
        self.allowed_channels=[0]

        # Listen for commands.
        self.recording = False
        self.store = Arctic('localhost')
        self.session_id = None
        self.library = None
        self.field_names = ['sys_time', 'bio_time', 'values', 'filt_values']

        # Set up the filter coefficients.
        self.freq_cutoff = freq_cutoff
        self.zi = {}
        for chn in self.allowed_channels:
            self.zi[chn] = np.zeros(self.filter_order)

    def config_database(self):
        '''Configure database.'''
        v = Vessel('db.cmd')
        if v.command == 'start_record':
            print('Recording started.')
            self.session_id = v.session_id
            if self.session_id not in self.store.list_libraries():
                self.store.initialize_library(self.session_id)
            self.library = self.store[self.session_id]
            self.recording = True
        elif v.command == 'stop_record':
            print('Recording stopped.')
            self.recording = False
            self.session_id = None

    def process(self, event):
        '''
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        '''
        # Raise an event with some data.
        if event.src_path == './db.cmd':
            self.config_database()
        else:
            data_loaded = False
            while not data_loaded:
                try:
                    data = Vessel(event.src_path)
                    data_loaded = True
                except:
                    print('File read fail!')

            # Filter and downsample!
            channel = data.channel_number
            v_filt, zi = lowpass(data.t, data.v, filter_order=self.filter_order,\
                    freq_cutoff=self.freq_cutoff, zi=self.zi[channel])
            self.zi[channel] = zi
            t_, v_ = downsample(data.t, v_filt, 100)
            package = {
                    '{:02d}-t'.format(channel): data.t,
                    '{:02d}-t_sys'.format(channel): data.t_sys,\
                    '{:02d}-v'.format(channel): data.v,\
                    '{:02d}-v_filt'.format(channel): v_filt}

            # Send data to the API.
            self.client.send_json([channel, v_])

            if self.recording:
                for (key, value) in package.items():
                    self.library.append(key, np.array(value))

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


class Watcher(object):
    '''Encapsulates watchdog process, exposing underlying event bus.'''

    def __init__(self):
        # Create Watchdog observer, etc.
        self.observer = Observer()
        self.buffer_processor = BufferProcessor()
        self.observer.schedule(self.buffer_processor, path='.')
        self.observer.start()

        # Extract the handler's event bus.
        self.events  = self.buffer_processor.events

if __name__ == '__main__':
    watcher = Watcher()
    # args = sys.argv[1:]
    # observer = Observer()
    # observer.schedule(BufferProcessor(), path=args[0] if args else '.')
    # observer.start()

    # h = observer._handlers
    # handler = list([v for k,v in h.items()][0])[0]

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.observer.stop()

    # observer.join()

