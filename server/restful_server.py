'''Back-end API for the annotation project.'''
from pyro.basics import *
from pymongo import MongoClient
from sixer import *


# Define application constants.
DATABASE_NAME = 'biomonitor'

# Connect to the database.
client = MongoClient()
database = client[DATABASE_NAME]

# Attach database to the Pyro framework.
Pyro.attach_db(database)

# Define application models.
class Session(Pyro):

    def after_new_model(self):
        '''Add a unique-ish, human readable name.'''
        self.hid = sixer()


# Boot the application!
server = Application(Pyro)
app = server.app

if __name__ == '__main__':
    app.run()



