from oracle import *
import os
from rest import *
from static import *
from subprocess import Popen
from time import sleep


# Main control loop for handling process launch, restarting failed servers...
# ----------------
# PORTS
# ----------------
# STATIC   - 5000
# REST API - 5100
# SOCK API - 5200
# ORACLE   - 5300

# 1. Serve the static site.
static_site = Popen(['python', 'static.py'])

# Serve the REST API.
rest_api = Popen(['python', 'rest.py'])

# Launch the UI's socket server.
sock_api = Popen(['python', 'sock.py'])

# Activate oracle.
oracle = Popen(['python', 'oracle.py'])

# Monitor processes. Shut down on keyboard break.
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print('Shutting down all processes...')
    static_site.kill()
    rest_api.kill()
    sock_api.kill()
    oracle.kill()

