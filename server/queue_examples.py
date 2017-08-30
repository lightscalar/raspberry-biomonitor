import numpy as np
from queue import Queue
import threading
from time import sleep


def process_data(q):
    '''Intensive IO.'''
    while True:
        data = q.get()
        print('Working on {:d}'.format(data))
        sleep(1.0)
        print('Task {:d} is complete.'.format(data))
        q.task_done()

q = Queue()
nb_workers = 10

for _ in range(nb_workers):
    worker = threading.Thread(target=process_data, args=(q,))
    worker.setDaemon(True)
    worker.start()

for itr in range(100):
    q.put(itr)

