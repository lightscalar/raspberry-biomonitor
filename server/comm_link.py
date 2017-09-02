import threading
import socket
from events import Events
import contextlib
import json


@contextlib.contextmanager
def accept(s):
    c,a = s.accept()
    print('client connected on',a)
    yield c,a
    print('client disconnected on',a)
    c.close()


class Server(threading.Thread):
    '''Socket server.'''

    def __init__(self, host='127.0.0.1', port=2048):
        '''Initialize host and port.'''
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.go = True
        self.events = Events()
        self.start()

    def run(self):
        '''Main loop of server thread.'''
        try:
            s = socket.socket()
            s.bind((self.host, self.port))
            s.listen(1)
            conn, _ = s.accept()
            while True:
                data = conn.recv(1024).decode()
                if data:
                    try:
                        obj = json.loads(data)
                        self.events.on_data_received(obj)
                    except:
                        pass
        finally:
            s.close()

    def close(self):
        self.go = False


class Client(object):

    def __init__(self, host='127.0.0.1', port=2048):
        '''Connect to the socket.'''
        self.port = port
        self.connected = False
        self.socket = socket.socket()
        try:
            self.socket.connect((host, port))
            self.connected = True
        except:
            print('Connection to port {} failed.'.format(port))

    def send(self, message):
        '''Send a message through socket.'''
        self.socket.send(message.encode())

    def send_json(self, message):
        '''Send a message through socket.'''
        self.socket.send(json.dumps(message).encode())

    def close(self):
        '''Close the connection.'''
        self.socket.close()

