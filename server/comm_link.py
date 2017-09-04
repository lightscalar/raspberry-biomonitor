import threading
import socket
from events import Events
import contextlib
import json
from time import sleep


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
        def recvall(sock):
            BUFF_SIZE = 4096 # 4 KiB
            data = ""
            while True:
                part = sock.recv(BUFF_SIZE).decode()
                data += part
                if len(part) < BUFF_SIZE:
                    # either 0 or end of data
                    break
            return data
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(1)
            conn, _ = s.accept()
            while True:
                # data = conn.recv(1024).decode()
                data = recvall(conn)
                if data:
                    try:
                        obj = json.loads(data)
                        self.events.on_data(obj)
                    except:
                        print('OOPS')
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
        while not self.connected:
            try:
                self.socket = socket.socket()
                self.socket.connect((host, port))
                self.connected = True
            except:
                print('Connection to port {} failed.'.format(port))
                sleep(0.5)
        print('Connection to port {} established.'.format(port))

    def send(self, message):
        '''Send a message through socket.'''
        self.socket.send(message.encode())

    def send_json(self, message):
        '''Send a message through socket.'''
        self.socket.send(json.dumps(message).encode())

    def close(self):
        '''Close the connection.'''
        self.socket.close()

