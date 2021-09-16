#!/usr/bin/env python3


import csv
import os
from datetime import datetime

import boto3

from utils.utils import parse_line

logs = boto3.client('logs')

LOG_GROUP = 'TEST-LOGS'
LOG_STREAM = 'stream1'

try:
    logs.create_log_group(logGroupName=LOG_GROUP)
except Exception as ex:
    print(f"Log group {LOG_GROUP} already exists")
    print(ex)

try:
    logs.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
except Exception as ex:
    print(f"Log stream {LOG_STREAM} already exists")
    print(ex)


CHUNK_SIZE = 10


def process_chunk(chunk):
    print("PROCESS CHUNK")
    logevents = [{
        'timestamp': int(line['date'].timestamp() * 1000),
        'message': f"{{'temp': {line['average_temp']}}}",
        } for line in chunk]

    print(datetime.utcfromtimestamp(int(chunk[0]['date'].timestamp() * 1000)/1000))
    response = logs.put_log_events(
        logGroupName=LOG_GROUP,
        logStreamName=LOG_STREAM,
        logEvents=logevents
    )
    print(response)


def main():
    with open(os.path.join('.', 'dly175.csv')) as file:
        csv_reader = csv.reader(file)
        chunk = []
        for i, row in enumerate(csv_reader):
            if (i % CHUNK_SIZE) == 0 and i > 0:
                if not chunk:
                    print('chunk empty continuing')
                    continue
                process_chunk(chunk)
                chunk = []
            if len(row) != 11 or row[0] == 'date':
                next(csv_reader)
                continue
            reading = parse_line(row)
            if reading is None:
                continue
            chunk.append(reading)


if __name__ == '__main__':
    main()
