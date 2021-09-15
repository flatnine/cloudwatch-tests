#!/usr/bin/env python3


import boto3
import csv
import os


from datetime import datetime

from utils.utils import calculate_average_temp, parse_line

logs = boto3.client('logs')

LOG_GROUP='TEST-LOGS'
LOG_STREAM='stream1'

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



# response = logs.put_log_events(
#     logGroupName=LOG_GROUP,
#     logStreamName=LOG_STREAM,
#     logEvents=[
#         {
#             'timestamp': timestamp,
#             'message': time.strftime('%Y-%m-%d %H:%M:%S')+'\tHello world, here is our first log message!'
#         }
#     ]
# )

def main():

    with open(os.path.join('.','dly175.csv')) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) != 11 or row[0] == 'date':
                next(csv_reader)
                continue
            reading = parse_line(row)
            if reading is None:
                continue
            print(f"{reading['date']} - {reading['average_temp']}")
            # put_metric(
            #     NAMESPACE, 
            #     METRIC_NAME, 
            #     DIMENSION_NAME, 
            #     DIMENSION_VALUE,
            #     reading)

if __name__ == '__main__':
    main() 