# cloudwatch-tests
Test adding data to Cloudwatch with Python Boto3 API 

Two scripts to read a CSV of tempreture data, transform and upload to Cloudwatch metrics.

`./metrics.py` - Uploads data to Metrics
`./logs.py` - Not complete but should load data to Cloudwatch logs.

This data will then be graphed and an Anomaly Detection alarm applied. Further data points will be added to see how Alarms are triggered.
