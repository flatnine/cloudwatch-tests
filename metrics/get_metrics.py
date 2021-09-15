#!/usr/bin/env python3

import boto3



NAMESPACE = 'Test Metric'
METRIC_NAME = 'Phoenix_Park_Temperature'
DIMENSION_NAME = 'Temperature'
DIMENSION_VALUE = 'Centigrade'


# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# List metrics through the pagination interface
paginator = cloudwatch.get_paginator('list_metrics')
for response in paginator.paginate(Dimensions=[{'Name': DIMENSION_NAME}],
                                   MetricName=METRIC_NAME,
                                   Namespace=NAMESPACE):
    print(response['Metrics'])