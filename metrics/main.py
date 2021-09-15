#!/usr/bin/env python3

import csv  
import boto3
import os 


from datetime import datetime, timedelta

NAMESPACE = 'Test Metric'
METRIC_NAME = 'Phoenix_Park_Temperature'
DIMENSION_NAME = 'Temperature'
DIMENSION_VALUE = 'Centigrade'

SIX_WEEKS_AGO = datetime.now() - timedelta(days = 42)
ONE_MONTH_AGO = datetime.now() - timedelta(days = 28)
ONE_MONTH = 28

client = boto3.client('cloudwatch')

def calculate_average_temp(min, max):
    return round((min + max) / 2, 2)

def transpose_date(date, days):
    """ Cloudwatch requires data within last two weeks """
    return date + timedelta(days=days)

def parse_line(row):
    line = {}
    parsed_date = datetime.strptime(row[0], '%d-%b-%Y')
    if parsed_date < SIX_WEEKS_AGO or parsed_date > ONE_MONTH_AGO:
        return

    line['date'] = transpose_date(parsed_date, ONE_MONTH)
    
    try:
        min_temp = float(row[4])
        max_temp = float(row[2])
    except ValueError:
        print('{row[4]} {row[2]} Cant be converted on {parsed_date}')
        min_temp = -273.15
        max_temp = -273.15
    line['average_temp'] = calculate_average_temp(min_temp ,max_temp)
    return line

def put_metric(namespace, metric_name, dimension_name, demension_metric, metric):
    result = client.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': metric_name,
                'Dimensions': [
                    {
                        'Name': dimension_name,
                        'Value': demension_metric,
                    },  
                ],
                'Timestamp': metric['date'],
                'Value': metric['average_temp'],
                'Unit': 'None',
            },
        ],
    )
    print(result)

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
        