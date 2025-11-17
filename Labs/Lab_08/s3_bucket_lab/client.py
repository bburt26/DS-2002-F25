import boto3

s3 = boto3.client('s3', region_name='us-east-1')

import boto3

s3 = boto3.client('s3', region_name='us-east-1')

bucket = 'ds2002-f25-jtg3ts'
local_file = 'lebron.png'   # correct path

with open(local_file, 'rb') as data:
    resp = s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=local_file
    )

