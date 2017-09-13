import eventlet
eventlet.monkey_patch()
from collections import deque
from threading import Thread
from time import sleep, time
from queue import Queue


class Antenna(object):
    '''Broadcasts data at specified data rate to a socket and thus the UI.'''

    def __init__(self, socket):
        '''Attach socket to object.'''
        Thread.__init__(self)
        self.socket = socket
        self.go = True
        self.queue = {}
        self.allowed_channels = [0, 1]
        for chn in self.allowed_channels:
            self.queue[chn] = deque([])
        # self.start()
        self.q = Queue()
        nb_workers = len(self.allowed_channels)
        target = self.push_data
        for _ in range(nb_workers):
            worker = Thread(target=target, args=(self.q,), daemon=True)
            worker.start()

    def push_data(self, q):
        '''Push data through the socket.'''
        while True:
            data = q.get()
            chn = data[0]
            package = list(zip(data[3], data[2]))
            package = [{'x': t, 'y': v} for (t,v) in zip(data[3], data[2])]
            if chn == 0:
                self.socket.emit('pzt', package)
            else:
                self.socket.emit('ppg', package)
            q.task_done()

    def stop(self):
        '''Stop main thread.'''
        self.go = False

    def push(self, data):
        '''Push data in channel's broadcast queue.
        INPUTS
            data - array_like
                data[0] - channel number
                data[1] - sampling rate
                data[2] - data samples
        '''
        self.q.put(data)
