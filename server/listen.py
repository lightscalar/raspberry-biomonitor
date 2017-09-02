from comm_link import *

s = Server(port=2048)
s.events.on_data_received = print
