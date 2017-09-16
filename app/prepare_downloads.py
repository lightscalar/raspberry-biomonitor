from datastore import DataStore
import datetime
import numpy as np
import pandas as pd
import os
import re
from solid_db import SolidDB
from zipfile import ZipFile


AVAILABLE_CHANNELS = ['PZT', 'PPG']
DOWNLOAD_LOCATION = '../static/downloads'
TMP_LOCATION = '.'


def parse_histories(histories):
    '''Cycle through histories and grab the latest version.'''
    history_dict = {}
    unique_histories = []
    for history in histories:
        history_dict[history['uid']] = history
    for key,val in history_dict.items():
        unique_histories.append(val)
    return unique_histories


def create_csv(session_id):
    '''Construct CSV files from recorded data and annotations.'''
    ds = DataStore()
    db = SolidDB('data/db.json')
    files_to_compress = []

    # Load the session from the database.
    session = db.find_by_id(session_id)
    human_id = session['hid'].upper()
    tstamp = session['createdAt']
    tstamp = re.sub(r"\s+", '_', tstamp)
    tstamp = tstamp.replace(':', '')

    # Read channel data and write to CSV files.
    for channel_number, channel_name in enumerate(AVAILABLE_CHANNELS):
        channel_data_present = False
        try:
            channel_data = ds.read_all(session_id, channel_number)
            channel_data_present = True
        except:
            pass

        if channel_data_present:
            filename = '{}/{}--{}--{}.csv'\
                    .format(TMP_LOCATION, tstamp, human_id, channel_name)
            df = pd.DataFrame(channel_data)
            df = df[['t', 't_sys', 'v', 'filtered']]
            df = df.rename(index=str, columns={'t': 'local_timestamp',\
                    't_sys': 'unix_timestamp', 'v': 'value',\
                    'filtered': 'filtered_value'})
            df.to_csv(filename)
            files_to_compress.append(filename)

    # Save annotation data. Two parts: Snapshots & Histories.
    filename = 'annotation.txt'
    files_to_compress.append(filename)
    with open(filename, 'w') as f:

        f.write('HISTORIES\n')
        f.write('---------\n\n')


        histories = parse_histories(session['histories'])
        for event in histories:
            f.write(event['name'] + ' -- ' + event['timestamp'] + '\n')
            f.write('---------------------------------------------------\n')
            if len(event['description']) > 0:
                f.write(event['description'] +'\n')
                f.write('---------------------------------------------------\n')

            fields = event['fields']
            for field in fields:
                if field['type'] == 'boolean':
                    field_len = len(field['name'])
                    tabs = '.' * int(30 - field_len)
                    f.write(field['name'] + ':'  + tabs + str(field['value']))
                    if len(field['units']) > 0:
                        f.write(' ('+field['units']+')')
                    if len(field['details'])>0:
                        f.write(' ' + '['+ field['details'] + ']')
                    f.write('\n')
                elif len(field['value']) > 0:
                    field_len = len(field['name'])
                    tabs = '.' * int(30 - field_len)
                    f.write(field['name'] + ':'  + tabs + field['value'])
                    if len(field['units']) > 0:
                        f.write(' ('+field['units']+')')
                    f.write('\n')
            f.write('\n\n')


        f.write('SNAPSHOTS\n')
        f.write('---------\n\n')

        for event in session['events']:
            f.write(event['name'] + ' -- ' + event['timestamp'] + '\n')
            f.write('---------------------------------------------------\n')
            if len(event['description']) > 0:
                f.write(event['description'] +'\n')
                f.write('---------------------------------------------------\n')

            fields = event['fields']
            for field in fields:
                if len(field['value']) > 0:
                    field_len = len(field['name'])
                    tabs = '.' * int(30 - field_len)
                    f.write(field['name'] + ':'  + tabs + field['value'])
                    if len(field['units']) > 0:
                        f.write(' ('+field['units']+')')
                    f.write('\n')
            f.write('\n\n')

    compressed_filename = '../static/downloads/{}_{}.zip'\
            .format(tstamp, human_id)

    with ZipFile(compressed_filename, 'w') as f:
        for filename in files_to_compress:
            f.write(filename)
            os.remove(filename)

    return compressed_filename






