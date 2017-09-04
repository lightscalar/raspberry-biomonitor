from collections import deque
from threading import Thread
from time import sleep, time


class Antenna(Thread):

    def __init__(self, socket):
        '''Attach socket to object.'''
        Thread.__init__(self)
        self.socket = socket
        self.go = True
        self.queue = {}
        self.allowed_channels = [0]
        for chn in self.allowed_channels:
            self.queue[chn] = deque([])
        self.start()

    def run(self):
        '''Main loop.'''
        q = self.queue
        while self.go:
            for chn in self.allowed_channels:
                if len(q[chn])>0:
                    val = self.queue[chn].popleft()
                    self.socket.emit('data_package', [chn, val])
            sleep(0.01) # 50 Hz

    def stop(self):
        '''Stop main thread.'''
        self.go = False

    def push(self, data):
        '''Push data in channel's broadcast queue.'''
        self.queue[data[0]].extend(data[1])
