import subprocess
from rest import *

if __name__ == '__main__':
    api = subprocess.Popen(['python', 'rest.py'])

    try:
        while True:
            pass
    except:
        print('Killing web service.')
        api.kill()


