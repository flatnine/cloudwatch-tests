#!/usr/bin/env python3

import csv
import os

import boto3

from utils.utils import parse_line

NAMESPACE = 'Test Metric'
METRIC_NAME = 'Phoenix_Park_Temperature'
DIMENSION_NAME = 'Temperature'
DIMENSION_VALUE = 'Centigrade'

client = boto3.client('cloudwatch')


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


def main():
    with open(os.path.join('.', 'dly175.csv')) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) != 11 or row[0] == 'date':
                next(csv_reader)
                continue
            reading = parse_line(row, True, True)
            if reading is None:
                continue
            print(f"{reading['date']} - {reading['average_temp']}")
            put_metric(
                NAMESPACE,
                METRIC_NAME,
                DIMENSION_NAME,
                DIMENSION_VALUE,
                reading)


if __name__ == '__main__':
    main()
