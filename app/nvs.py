import os
from subprocess import Popen
from time import sleep

# Main control loop for handling process launch, restarting failed servers...

# 1. Serve the static site.
static_site = Popen(['python', 'static.py'])

# Serve the REST API.
rest_api = Popen(['python', 'rest.py'])

# Activate Biomonitor process.
data_collector = Popen(['python', 'data_source.py'])

# Monitor processes. Shut down on keyboard break.
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print('Shutting down all processes...')
    static_site.kill()
    rest_api.kill()
    data_collector.kill()

